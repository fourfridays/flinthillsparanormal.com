"""Targeted filters for expected Sentry events."""


def filter_sentry_event(event, hint):
    if event.get("logger") == "django.security.DisallowedHost":
        return None

    record = hint.get("log_record")
    if (
        record is not None
        and record.name == "gunicorn.http.wsgi"
        and record.getMessage()
        == "WSGI app sent body bytes on a no-body response "
        "(method=HEAD status=200); dropping per RFC 9110."
    ):
        # Django leaves HEAD body stripping to the server. Gunicorn does so
        # correctly, but warns about this expected behavior.
        return None

    return event
