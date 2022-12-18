from flask_apispec.views import MethodResource
from flask import jsonify


class BaseView(MethodResource):
    @classmethod
    def register(cls, blueprint, spec, url, name):
        blueprint.add_url_rule(url, view_func=cls.as_view(name))
        blueprint.register_error_handler(422, cls.handle_error)
        spec.register(cls, blueprint=blueprint.name)

    @staticmethod
    def handle_error(err):
        headers = err.data.get('headers', None)
        messages = err.data.get('messages', ['Invalid request'])
        if headers:
            return jsonify({'message': messages}), 400, headers
        else:
            return jsonify({'message': messages}), 400
