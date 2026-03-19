import flask 
from flask import jsonify
from flask import request
import datetime
#noinspection ImportError
from . import db_session # как решить конфликт Exception has occurred: ImportError attempted relative import with no known parent package?
from flask import make_response
from . import jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    ds_sess = db_session.create_session()
    jobs_list = ds_sess.query(jobs.Jobs).all()
    return jsonify(
            {
                'jobs':
                [item.to_dict()for item in jobs_list]
            }
        )


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_job(job_id):
    ds_sess = db_session.create_session()
    job = ds_sess.query(jobs.Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
            {
                'job': job.to_dict()
            }
        )
    

@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def create_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size',
                                                 'collaborators', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    ds_sess = db_session.create_session()
    if ds_sess.query(jobs.Jobs).get(job_id):
        return make_response(jsonify({'error': 'Id already exists'}), 400)
    job = jobs.Jobs(
        id=job_id,
        team_leader=request.json.get('team_leader'),
        job=request.json.get('job'),
        work_size=request.json.get('work_size'),
        collaborators=request.json.get('collaborators'),
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        is_finished=request.json.get('is_finished')
    )
    ds_sess.add(job)
    ds_sess.commit()
    return jsonify(
            {
                'success': 'OK'
            }
         )
    
'''Напишите обработчик для удаления работы по id.'''
@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    ds_sess = db_session.create_session()
    job = ds_sess.query(jobs.Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    ds_sess.delete(job)
    ds_sess.commit()
    return jsonify(
            {
                'success': 'OK'
            }
         )
    
@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    ds_sess = db_session.create_session()
    job = ds_sess.query(jobs.Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)
    ds_sess.commit()
    return jsonify(
            {
                'success': 'OK'
            }
         )