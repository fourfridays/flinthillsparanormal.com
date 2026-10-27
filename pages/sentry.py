"""Targeted filters for expected Sentry events."""

import logging

_GUNICORN_NO_BODY_WARNING = (
    "WSGI app sent body bytes on a no-body response "
    "(method=%s status=%s); dropping per RFC 9110."
)


def filter_sentry_event(event, hint):
    if event.get("logger") == "django.security.DisallowedHost":
        return None

    record = hint.get("log_record")
    if (
        record is not None
        and record.name == "gunicorn.http.wsgi"
        and record.levelno == logging.WARNING
        and record.msg == _GUNICORN_NO_BODY_WARNING
        and isinstance(record.args, tuple)
        and len(record.args) == 2
    ):
        # Gunicorn supplies (method, status) as logging arguments, not extra
        # fields or an event code. Match the template to identify this warning
        # without parsing rendered text. Unknown signatures are kept.
        method, status = record.args
        if method == "HEAD" and isinstance(status, int) and 200 <= status < 500:
            # Django leaves HEAD body stripping to the server. Suppress that
            # expected warning, but retain it for server-error responses.
            return None

    return event
