from flask_restful import Resource, abort
from flask import jsonify, make_response, request
from . import db_session


class UsersResource(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if not user:
            abort(404, message=f"User {user_id} not found")
        return jsonify(
            {
                'user': user.to_dict()
            }
         )


class UsersListResource(Resource):
    pass

