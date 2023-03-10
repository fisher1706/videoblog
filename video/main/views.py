from flask import Blueprint, jsonify
from video import logger, docs
from video.schemas import VideoSchema
from flask_apispec import use_kwargs, marshal_with
from video.models import Video
from flask_jwt_extended import jwt_required, get_jwt_identity
from video.base_view import BaseView


videos = Blueprint('videos', __name__)


class ListView(BaseView):
    @marshal_with(VideoSchema(many=True))
    def get(self):
        try:
            videos = Video.get_list()
        except Exception as e:
            logger.warning(f'tutorials - read action with errors: {e}')
            return {'message': str(e)}, 400

        return videos


@videos.route('/')
def main():
    return 'it works'


@videos.route('/tutorials', methods=['GET'])
@jwt_required()
@marshal_with(VideoSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()

        # only for test log
        # raise Exception('Test Error')

        videos = Video.get_user_list(user_id=user_id)
    except Exception as e:
        logger.warning(f'user: {user_id} tutorials - read action failed with errors: {e}')
        return {'message': str(e)}, 400

    return videos


@videos.route('/tutorials', methods=['POST'])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
    user_id = None

    try:
        user_id = get_jwt_identity()
        new_one = Video(user_id=user_id, **kwargs)
        new_one.save()
    except Exception as e:
        logger.warning(f'user: {user_id} tutorials - create action failed with errors: {e}')
        return {'message': str(e)}, 400

    return new_one


@videos.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_tutorial(tutorial_id, **kwargs):
    try:
        from flask import request
        params = request.json
        print(f'\nparams: {params}')

        user_id = get_jwt_identity()
        item = Video.get(tutorial_id, user_id)
        print(f'\nitem_id: {item.id}')

        item.update(**kwargs)
    except Exception as e:
        logger.warning(f'user:{user_id} tutorial:{tutorial_id} - update action failed with errors: {e}')
        return {'message': str(e)}, 400

    return item


@videos.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required()
@marshal_with(VideoSchema)
def delete_tutorial(tutorial_id):
    try:
        user_id = get_jwt_identity()
        item = Video.get(tutorial_id, user_id)
        item.delete()
    except Exception as e:
        logger.warning(f'user:{user_id} tutorial:{tutorial_id} - delete action failed with errors: {e}')
        return {'message': str(e)}, 400

    return '', 204


@videos.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='videos')
docs.register(update_list, blueprint='videos')
docs.register(update_tutorial, blueprint='videos')
docs.register(delete_tutorial, blueprint='videos')

ListView.register(videos, docs, '/main', 'listview')
