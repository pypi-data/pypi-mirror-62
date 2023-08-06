import functools
from collections import Iterable, namedtuple

from flask import Blueprint, jsonify, Response, abort

from veripress.helpers import url_rule

api_blueprint = Blueprint('api', __name__)


class Error(object):
    """
    Defines API error codes and error messages.
    """

    _Error = namedtuple('Error', ('code', 'msg', 'status_code'))

    UNDEFINED = _Error(100, 'Undefined error.', 400)
    NO_SUCH_API = _Error(101, 'No such API.', 404)
    RESOURCE_NOT_EXISTS = _Error(102, 'The resource does not exist.', 404)
    INVALID_ARGUMENTS = _Error(103, 'Invalid argument(s).', 400)
    NOT_ALLOWED = _Error(104, 'The resource path is not allowed.', 403)
    BAD_PATH = _Error(105, 'The resource path cannot be recognized.', 400)


class ApiException(Exception):
    """Raised by API functions when something goes wrong."""

    def __init__(self, message=None, error=Error.UNDEFINED,
                 status_code=None, payload=None):
        super(ApiException, self).__init__()
        self.message = message
        self.status_code = status_code
        self.error = error
        self.payload = payload

    def to_dict(self):
        result = dict(self.payload or {})
        result['code'] = self.error.code
        result['message'] = self.message or self.error.msg
        return result


@api_blueprint.errorhandler(ApiException)
def handle_api_exception(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code or e.error.status_code
    return response


@api_blueprint.errorhandler(404)
def handle_page_not_found(e):
    return handle_api_exception(ApiException(error=Error.NO_SUCH_API))


def json_api(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ApiException(error=Error.RESOURCE_NOT_EXISTS)

        if isinstance(result, Response):
            return result

        try:
            return jsonify(result)
        except TypeError as e:
            if isinstance(result, Iterable):
                return jsonify(list(result))
            else:
                raise e

    return wrapper


from veripress.api import handlers


def rule(rules, strict_slashes=False, api_func=None, *args, **kwargs):
    """
    Add a API route to the 'api' blueprint.

    :param rules: rule string or string list
    :param strict_slashes: same to Blueprint.route, but default value is False
    :param api_func: a function that returns a JSON serializable object
                     or a Flask Response, or raises ApiException
    :param args: other args that should be passed to Blueprint.route
    :param kwargs: other kwargs that should be passed to Blueprint.route
    :return:
    """
    return url_rule(api_blueprint, rules, strict_slashes=strict_slashes,
                    view_func=json_api(api_func) if api_func else None,
                    *args, **kwargs)


rule('/site', endpoint='site', api_func=handlers.site_info, methods=['GET'])
rule(['/posts',
      '/posts/<int:year>',
      '/posts/<int:year>/<int:month>',
      '/posts/<int:year>/<int:month>/<int:day>',
      '/posts/<int:year>/<int:month>/<int:day>/<string:post_name>'],
     api_func=handlers.posts, methods=['GET'])
rule('/tags', api_func=handlers.tags, methods=['GET'])
rule('/categories', api_func=handlers.categories, methods=['GET'])
rule('/widgets', api_func=handlers.widgets, methods=['GET'])
rule('/pages/<path:page_path>', api_func=handlers.pages, methods=['GET'],
     strict_slashes=True)
rule('/search', api_func=handlers.search, methods=['GET'])

# direct all unknown paths to 404
rule('/<path:_>', api_func=lambda _: abort(404), methods=['GET'])
