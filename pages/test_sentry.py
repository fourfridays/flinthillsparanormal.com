import logging
import unittest

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

    def test_drops_expected_head_warning(self):
        record = self.make_record()
        event = {"logger": record.name}
        self.assertIsNone(filter_sentry_event(event, {"log_record": record}))

    def test_preserves_other_methods_statuses_and_loggers(self):
        for overrides in (
            {"method": "GET", "status": 204},
            {"status": 500},
            {"name": "another.logger"},
        ):
            with self.subTest(**overrides):
                record = self.make_record(**overrides)
                event = {"logger": record.name}
                self.assertIs(
                    filter_sentry_event(event, {"log_record": record}), event
                )

    def test_preserves_unrelated_gunicorn_warning(self):
        record = self.make_record()
        record.msg = "Unrelated Gunicorn warning"
        record.args = ()
        event = {"logger": record.name}
        self.assertIs(filter_sentry_event(event, {"log_record": record}), event)

    def test_preserves_events_without_log_records(self):
        event = {"message": "Application error"}
        self.assertIs(filter_sentry_event(event, {}), event)

    def test_still_drops_disallowed_host(self):
        event = {"logger": "django.security.DisallowedHost"}
        self.assertIsNone(filter_sentry_event(event, {}))
