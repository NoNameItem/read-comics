import json
import logging
from functools import partial, wraps

from crum import get_current_user
from django.core.exceptions import EmptyResultSet
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.response import TemplateResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response

SUCCESS = 25


class ReprEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if isinstance(o, QuerySet):
                try:
                    return str(o.query)
                except EmptyResultSet:
                    return "empty"
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return repr(o)


class Logger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


def getLogger(name="default"):
    logging.addLevelName(SUCCESS, "SUCCESS")
    logging.setLoggerClass(Logger)
    return logging.getLogger("read_comics." + name)


class LogUserFilter(logging.Filter):
    def filter(self, record):
        user = get_current_user()
        if user:
            record.username = user.username
        else:
            record.username = "-"
        return True


def log_value(arg):
    arg_type = type(arg)
    if isinstance(arg, QuerySet):
        arg = {"db": arg.db, "query": str(arg.query)}
    if isinstance(arg, DRFRequest):
        _resolver_match = arg._request.resolver_match  # noqa
        if _resolver_match:
            resolver_match = {
                "route": _resolver_match.route,
                "url_name": _resolver_match.url_name,
                "view_name": _resolver_match.view_name,
                "args": _resolver_match.args,
                "kwargs": _resolver_match.kwargs,
            }
        else:
            resolver_match = None
        arg = {
            "method": arg._request.method,  # noqa
            "path": arg._request.path,  # noqa
            "resolver_match": resolver_match,
            "data": arg.data,
            "has_files": len(arg.FILES) > 0,
            "user": str(arg.user),
        }
    elif isinstance(arg, HttpRequest):
        _resolver_match = arg.resolver_match
        if _resolver_match:
            resolver_match = {
                "route": _resolver_match.route,
                "url_name": _resolver_match.url_name,
                "view_name": _resolver_match.view_name,
                "args": _resolver_match.args,
                "kwargs": _resolver_match.kwargs,
            }
        else:
            resolver_match = None
        arg = {
            "method": arg.method,
            "path": arg.path,
            "resolver_match": resolver_match,
            "GET": dict(arg.GET.lists()),
            "POST": dict(arg.POST.lists()),
            "has_files": len(arg.FILES) > 0,
            "user": str(arg.user),
        }
    elif isinstance(arg, TemplateResponse):
        arg = {"template_name": arg.template_name, "context_data": arg.context_data}
    elif isinstance(arg, Response):
        arg = {
            "status_code": arg.status_code,
            "status_text": arg.status_text,
            "content_type": arg.content_type,
            "data": arg.data,
        }
    try:
        arg_str = json.dumps(arg, indent=2, ensure_ascii=False, cls=ReprEncoder)
    except TypeError:
        arg_str = repr(arg)
    return arg_str, arg_type


def logged(logger, function_name=None, trace=False, unhandled_error_level=logging.WARNING, **kwargs_dec):
    def decorator(func):
        name = function_name or str(func).split(" ")[1]

        @wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug(f">>> Starting {name}")
            for i in range(len(args)):
                arg = args[i]
                arg_str, arg_type = log_value(arg)
                logger.debug(f">>> {name} args[{i}]({arg_type}):\n{arg_str}\n")
            for key, value in kwargs.items():
                arg_str, arg_type = log_value(value)
                logger.debug(f">>> {name} {key}({arg_type}):\n{arg_str}\n")
            try:
                result = func(*args, **kwargs)
                result_str, result_type = log_value(result)
                logger.debug(f"Successfully ended {name}")
                logger.debug(f"{name} return value ({result_type}): \n{result_str}\n")
                return result
            except Exception as e:
                logger.log(
                    unhandled_error_level,
                    f'Unhandled exception in {name}: "{repr(e)}". It may be handled later, '
                    f"but check django logs for all unhandled errors",
                    exc_info=trace,
                )
                raise
            finally:
                logger.debug(f"<<< Exiting {name}")

        return wrapped

    return decorator


def methods_logged(logger, methods=None):
    _decorator = partial(logged, logger)

    def class_decorator(cls):
        if not isinstance(cls, type):
            raise TypeError(f"Decorator `methods_logged` should be used on class. Got {cls} instead")

        if not methods:
            _methods = [
                (getattr(cls, x), x, {"function_name": f"{cls.__name__}.{x}"})
                for x in dir(cls)
                if (not x.startswith("__")) and callable(getattr(cls, x)) and (not isinstance(getattr(cls, x), type))
            ]
        else:
            _methods = []
            for method in methods:
                if isinstance(method, str):
                    method_name = method
                    method_conf = {"function_name": f"{cls.__name__}.{method_name}"}
                else:
                    try:
                        method_name = method[0]
                        if not isinstance(method[1], dict):
                            raise ValueError()
                        method_conf = method[1]
                        method_conf["function_name"] = method_conf.get("function_name", f"{cls.__name__}.{method_name}")
                    except (TypeError, ValueError):
                        raise ValueError(
                            "Elements of keyword argument `methods` must be either names of methods or tuples "
                            f"(<name of method>, <logging parameters>). Got {method} instead"
                        )
                if not (method_name and hasattr(cls, method_name)):
                    raise ValueError(
                        "The keyword argument `methods` must contain names of a methods "
                        f"of the decorated class: {cls}. Got '{method_name}' instead."
                    )
                _method = getattr(cls, method_name)
                if not callable(_method):
                    raise TypeError(
                        f"Cannot decorate '{method_name}' as it isn't a callable attribute of " f"{cls} ({_method})."
                    )
                _methods.append((_method, method_name, method_conf))

        for method, method_name, method_conf in _methods:
            _wrapped = _decorator(**method_conf)(method)
            setattr(cls, method_name, _wrapped)

        return cls

    return class_decorator
