from flask import request
from flask_restful import Resource


class Hello(Resource):

    def get(self):
        return "Haribol!"

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'msg': 'No input data provided'}, 400
