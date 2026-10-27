import logging
import unittest
from unittest.mock import Mock

from gunicorn.config import Config
from gunicorn.http.wsgi import Response

from pages.sentry import filter_sentry_event


class SentryEventFilterTests(unittest.TestCase):
    def make_record(self, method="HEAD", status=200, name="gunicorn.http.wsgi"):
        return logging.LogRecord(
            name,
            logging.WARNING,
            __file__,
            1,
            "WSGI app sent body bytes on a no-body response "
            "(method=%s status=%s); dropping per RFC 9110.",
            (method, status),
            None,
        )

    def test_drops_expected_head_warnings_across_non_server_error_statuses(self):
        for status in (200, 201, 204, 301, 302, 304, 400, 403, 404, 405, 429, 499):
            with self.subTest(status=status):
                record = self.make_record(status=status)
                event = {"logger": record.name}
                self.assertIsNone(filter_sentry_event(event, {"log_record": record}))

    def test_preserves_other_methods_statuses_and_loggers(self):
        for method, status, name in (
            ("GET", 204, "gunicorn.http.wsgi"),
            ("GET", 304, "gunicorn.http.wsgi"),
            ("POST", 200, "gunicorn.http.wsgi"),
            ("HEAD", 199, "gunicorn.http.wsgi"),
            ("HEAD", 500, "gunicorn.http.wsgi"),
            ("HEAD", 503, "gunicorn.http.wsgi"),
            ("HEAD", 200, "another.logger"),
        ):
            with self.subTest(method=method, status=status, name=name):
                record = self.make_record(method=method, status=status, name=name)
                event = {"logger": record.name}
                self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_preserves_unrelated_gunicorn_warning(self):
        record = self.make_record()
        record.msg = "Unrelated Gunicorn warning"
        record.args = ()
        event = {"logger": record.name}
        self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_preserves_unrelated_warning_with_same_arguments(self):
        record = self.make_record()
        record.msg = "Another warning (method=%s status=%s)"
        event = {"logger": record.name}
        self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_preserves_unexpected_argument_shapes(self):
        for args in (
            (),
            ("HEAD",),
            ("HEAD", "200"),
            ("HEAD", None),
            ("HEAD", 200, "extra"),
            {"method": "HEAD", "status": 200},
        ):
            with self.subTest(args=args):
                record = self.make_record()
                record.args = args
                event = {"logger": record.name}
                self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_preserves_error_records(self):
        record = self.make_record()
        record.levelno = logging.ERROR
        record.levelname = "ERROR"
        event = {"logger": record.name}
        self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_matches_real_gunicorn_warning(self):
        # Exercise the installed dependency so an upstream signature change
        # fails this test rather than silently making the filter ineffective.
        request = Mock(method="HEAD", version=(1, 1))
        request.should_close.return_value = False
        response = Response(request, Mock(), Config())
        response.start_response("403 Forbidden", [("Content-Length", "4")])
        with self.assertLogs("gunicorn.http.wsgi", level=logging.WARNING) as logs:
            response.write(b"body")
        self.assertEqual(len(logs.records), 1)
        record = logs.records[0]
        event = {"logger": record.name}
        self.assertIsNone(filter_sentry_event(event, {"log_record": record}))

    def test_preserves_events_without_log_records(self):
        event = {"message": "Application error"}
        self.assertIs(filter_sentry_event(event, {}), event)

    def test_still_drops_disallowed_host(self):
        event = {"logger": "django.security.DisallowedHost"}
        self.assertIsNone(filter_sentry_event(event, {}))
