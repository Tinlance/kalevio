import pytest
from backend.compliance.frameworks.nis2 import NIS2_ARTICLE_21_MEASURES, calculate_compliance_score, get_csirt, CSIRT_ENDPOINTS

class TestNIS2:
    def test_ten_measures(self):
        assert len(NIS2_ARTICLE_21_MEASURES) == 10

    def test_weights_sum_100(self):
        assert sum(m["weight"] for m in NIS2_ARTICLE_21_MEASURES) == 100

    def test_zero_score(self):
        assert calculate_compliance_score({}) == 0

    def test_full_score(self):
        assert calculate_compliance_score({m["id"]: "compliant" for m in NIS2_ARTICLE_21_MEASURES}) == 100

    def test_partial_score(self):
        s = calculate_compliance_score({"a": "compliant"})
        assert 0 < s < 100

    def test_estonia_csirt(self):
        assert "cert.ee" in get_csirt("EE")["email"]

    def test_fallback_to_estonia(self):
        assert get_csirt("XX") == CSIRT_ENDPOINTS["EE"]

    def test_ten_csirts(self):
        assert len(CSIRT_ENDPOINTS) >= 10
