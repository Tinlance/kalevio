from datetime import datetime, timezone, timedelta

class TestNIS2Deadlines:
    def test_24h_early_warning(self):
        now = datetime.now(timezone.utc)
        assert abs((now + timedelta(hours=24) - now).total_seconds() - 86400) < 1

    def test_72h_notification(self):
        now = datetime.now(timezone.utc)
        assert abs((now + timedelta(hours=72) - now).total_seconds() - 259200) < 1

    def test_30d_final_report(self):
        now = datetime.now(timezone.utc)
        assert abs((now + timedelta(days=30) - now).total_seconds() - 2592000) < 1

    def test_deadline_order(self):
        now = datetime.now(timezone.utc)
        ew = now + timedelta(hours=24)
        notif = now + timedelta(hours=72)
        final = now + timedelta(days=30)
        assert ew < notif < final

class TestSeverity:
    def test_critical(self):
        from api.routes.incidents import classify_severity
        from models.incident import IncidentSeverity
        assert classify_severity(14.76) == IncidentSeverity.CRITICAL

    def test_high(self):
        from api.routes.incidents import classify_severity
        from models.incident import IncidentSeverity
        assert classify_severity(7.01) == IncidentSeverity.HIGH

    def test_medium(self):
        from api.routes.incidents import classify_severity
        from models.incident import IncidentSeverity
        assert classify_severity(3.89) == IncidentSeverity.MEDIUM

    def test_low(self):
        from api.routes.incidents import classify_severity
        from models.incident import IncidentSeverity
        assert classify_severity(1.0) == IncidentSeverity.LOW
