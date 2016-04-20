import json
from functools import wraps
from utils import _get_lang
from .utils import error_response


def inject_lang(view):

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        kwargs['lang'] = _get_lang(request)
        return view(request, *args, **kwargs)

    return wrapper


def inject_json_data(view):

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if 'application/json' not in request.META['CONTENT_TYPE']:
            return error_response(
                {'error': 'Expected content type: "application/json".'},
                400
            )
        try:
            kwargs['json_data'] = json.loads(request.body)
        except ValueError:
            return error_response(
                {'error': 'No JSON object could be decoded.'},
                400
            )
        return view(request, *args, **kwargs)

    return wrapper

def require_params(*items):

    def real_decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            print kwargs
            for item in items:
                if item not in kwargs['json_data']:
                    return error_response(
                        {'error': 'Expected parameter {}'.format(item)},
                        status=400
                    )

            return view(request, *args, **kwargs)
        return wrapper

    return real_decorator
