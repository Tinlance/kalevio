import pytest
from backend.detection.threatfade import ThreatFadeEngine

@pytest.fixture
def engine():
    return ThreatFadeEngine(zscore_threshold=2.5)

class TestThreatFadeEngine:
    def test_clean_traffic_no_threat(self, engine):
        r = engine.analyze_features({"packet_sizes": [512,513,511,514,512]})
        assert r.threat_detected == False

    def test_empty_features_no_threat(self, engine):
        r = engine.analyze_features({})
        assert r.z_score == 0.0 and r.packet_count == 0

    def test_result_has_required_fields(self, engine):
        r = engine.analyze_features({"packet_sizes": [512]})
        assert hasattr(r, 'threat_detected') and hasattr(r, 'z_score')
        assert hasattr(r, 'mitre_ttps') and isinstance(r.mitre_ttps, list)

    def test_confidence_bounded(self, engine):
        r = engine.analyze_features({"packet_sizes": [1,10000,1,10000]})
        assert 0.0 <= r.confidence <= 1.0

    def test_z_score_non_negative(self, engine):
        r = engine.analyze_features({"packet_sizes": [512,256,1024]})
        assert r.z_score >= 0.0

    def test_source_ip_preserved(self, engine):
        r = engine.analyze_features({"packet_sizes": [512], "source_ip": "192.168.1.1"})
        assert r.source_ip == "192.168.1.1"
