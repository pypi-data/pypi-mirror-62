"""Flask web application views."""
import datetime
import re

from astropy.time import Time
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask import make_response
from requests.exceptions import HTTPError
import pkg_resources

from . import app as celery_app
from ._version import get_versions
from .flask import app, cache
from .tasks import first2years, gracedb, orchestrator, circulars, superevents


@app.route('/')
def index():
    """Render main page."""
    return render_template(
        'index.jinja2',
        conf=celery_app.conf,
        packages=pkg_resources.working_set,
        versions=get_versions())


def take_n(n, iterable):
    """Take the first `n` items of a collection."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item


# Regular expression for parsing query strings
# that look like GraceDB superevent names.
_typeahead_superevent_id_regex = re.compile(
    r'(?P<prefix>[MT]?)S?(?P<date>\d{0,6})(?P<suffix>[a-z]*)',
    re.IGNORECASE)


@app.route('/typeahead_superevent_id')
@cache.cached(query_string=True)
def typeahead_superevent_id():
    """Search GraceDB for superevents by ID.

    This involves some date parsing because GraceDB does not support directly
    searching for superevents by ID substring.
    """
    max_results = 8  # maximum number of results to return
    batch_results = 32  # batch size for results from server

    term = request.args.get('superevent_id')
    match = _typeahead_superevent_id_regex.fullmatch(term) if term else None

    if match:
        # Determine GraceDB event category from regular expression.
        prefix = match['prefix'].upper() + 'S'
        category = {'T': 'test', 'M': 'MDC'}.get(
            match['prefix'].upper(), 'production')

        # Determine start date from regular expression by padding out
        # the partial date with missing digits defaulting to 000101.
        date_partial = match['date']
        date_partial_length = len(date_partial)
        try:
            date_start = datetime.datetime.strptime(
                date_partial + '000101'[date_partial_length:], '%y%m%d')
        except ValueError:  # invalid date
            return jsonify([])

        # Determine end date from regular expression by adding a very
        # loose upper bound on the number of days until the next
        # digit in the date rolls over. No need to be exact here.
        date_end = date_start + datetime.timedelta(
            days=[36600, 3660, 366, 320, 32, 11, 1.1][date_partial_length])

        # Determine GraceDB event suffix from regular expression.
        suffix = match['suffix'].lower()
    else:
        prefix = 'S'
        category = 'production'
        date_end = datetime.datetime.utcnow()
        date_start = date_end - datetime.timedelta(days=7)
        date_partial = ''
        date_partial_length = 0
        suffix = ''

    # Query GraceDB.
    query = 'category: {} t_0: {} .. {}'.format(
        category, Time(date_start).gps, Time(date_end).gps)
    response = gracedb.client.superevents.search(
        query=query, sort='superevent_id', count=batch_results)

    # Filter superevent IDs that match the search term.
    regex = re.compile(r'{}{}\d{{{}}}{}[a-z]*'.format(
        prefix, date_partial, 6 - date_partial_length, suffix))
    superevent_ids = (
        superevent['superevent_id'] for superevent
        in response if regex.fullmatch(superevent['superevent_id']))

    # Return only the first few matches.
    return jsonify(list(take_n(max_results, superevent_ids)))


@app.route('/typeahead_event_id')
@cache.cached(query_string=True)
def typeahead_event_id():
    """Search GraceDB for events by ID."""
    superevent_id = request.args.get('superevent_id').strip()
    query_terms = [f'superevent: {superevent_id}']
    if superevent_id.startswith('T'):
        query_terms.append('Test')
    elif superevent_id.startswith('M'):
        query_terms.append('MDC')
    query = ' '.join(query_terms)
    try:
        results = gracedb.get_events(query)
    except HTTPError:
        results = []
    results = [dict(r, snr=superevents.get_snr(r)) for r in results
               if superevents.is_complete(r)]
    return jsonify(list(reversed(sorted(results, key=superevents.keyfunc))))


def _search_by_tag_and_filename(superevent_id, filename, extension, tag):
    try:
        records = gracedb.get_log(superevent_id)
        return [
            '{},{}'.format(record['filename'], record['file_version'])
            for record in records if tag in record['tag_names']
            and record['filename'].startswith(filename)
            and record['filename'].endswith(extension)]
    except HTTPError as e:
        # Ignore 404 errors from server
        if e.response.status_code == 404:
            return []
        else:
            raise


@app.route('/typeahead_skymap_filename')
@cache.cached(query_string=True)
def typeahead_skymap_filename():
    """Search for sky maps by filename."""
    return jsonify(_search_by_tag_and_filename(
        request.args.get('superevent_id') or '',
        request.args.get('filename') or '',
        '.fits.gz', 'sky_loc'
    ))


@app.route('/typeahead_em_bright_filename')
@cache.cached(query_string=True)
def typeahead_em_bright_filename():
    """Search em_bright files by filename."""
    return jsonify(_search_by_tag_and_filename(
        request.args.get('superevent_id') or '',
        request.args.get('filename') or '',
        '.json', 'em_bright'
    ))


@app.route('/typeahead_p_astro_filename')
@cache.cached(query_string=True)
def typeahead_p_astro_filename():
    """Search p_astro files by filename."""
    return jsonify(_search_by_tag_and_filename(
        request.args.get('superevent_id') or '',
        request.args.get('filename') or '',
        '.json', 'p_astro'
    ))


@app.route('/send_preliminary_gcn', methods=['POST'])
def send_preliminary_gcn():
    """Handle submission of preliminary alert form."""
    keys = ('superevent_id', 'event_id')
    superevent_id, event_id, *_ = tuple(request.form.get(key) for key in keys)
    if superevent_id and event_id:
        (
            gracedb.upload.s(
                None, None, superevent_id,
                'User {} queued a Preliminary alert through the dashboard.'
                .format(request.remote_user or '(unknown)'),
                tags=['em_follow'])
            |
            gracedb.update_superevent.si(
                superevent_id, preferred_event=event_id)
            |
            gracedb.get_event.si(event_id)
            |
            orchestrator.preliminary_alert.s(superevent_id)
        ).delay()
        flash('Queued preliminary alert for {}.'.format(superevent_id),
              'success')
    else:
        flash('No alert sent. Please fill in all fields.', 'danger')
    return redirect(url_for('index'))


@app.route('/change_prefered_event', methods=['POST'])
def change_prefered_event():
    """Handle submission of preliminary alert form."""
    keys = ('superevent_id', 'event_id')
    superevent_id, event_id, *_ = tuple(request.form.get(key) for key in keys)
    if superevent_id and event_id:
        (
            gracedb.upload.s(
                None, None, superevent_id,
                'User {} queued a prefered event change to {}.'
                .format(request.remote_user or '(unknown)', event_id),
                tags=['em_follow'])
            |
            gracedb.update_superevent.si(
                superevent_id, preferred_event=event_id)
            |
            gracedb.get_event.si(event_id)
            |
            orchestrator.preliminary_alert.s(
                superevent_id, initiate_voevent=False)
        ).delay()
        flash('Changed prefered event for {}.'.format(superevent_id),
              'success')
    else:
        flash('No change performed. Please fill in all fields.', 'danger')
    return redirect(url_for('index'))


@app.route('/send_update_gcn', methods=['POST'])
def send_update_gcn():
    """Handle submission of update alert form."""
    keys = ('superevent_id', 'skymap_filename',
            'em_bright_filename', 'p_astro_filename')
    superevent_id, *filenames = args = tuple(
        request.form.get(key) for key in keys)
    if all(args):
        (
            gracedb.upload.s(
                None, None, superevent_id,
                'User {} queued an Update alert through the dashboard.'
                .format(request.remote_user or '(unknown)'),
                tags=['em_follow'])
            |
            orchestrator.update_alert.si(filenames, superevent_id)
        ).delay()
        flash('Queued update alert for {}.'.format(superevent_id), 'success')
    else:
        flash('No alert sent. Please fill in all fields.', 'danger')
    return redirect(url_for('index'))


@app.route('/create_update_gcn_circular', methods=['POST'])
def create_update_gcn_circular():
    """Handle submission of GCN Circular form."""
    keys = ['sky_localization', 'em_bright', 'p_astro']
    superevent_id = request.form.get('superevent_id')
    updates = [key for key in keys if request.form.get(key)]
    if superevent_id and updates:
        response = make_response(circulars.create_update_circular(
            superevent_id,
            update_types=updates))
        response.headers["content-type"] = "text/plain"
        return response
    else:
        flash('No circular created. Please fill in superevent ID and at ' +
              'least one update type.', 'danger')
    return redirect(url_for('index'))


@app.route('/send_mock_event', methods=['POST'])
def send_mock_event():
    """Handle submission of mock alert form."""
    first2years.upload_event.delay()
    flash('Queued a mock event.', 'success')
    return redirect(url_for('index'))
