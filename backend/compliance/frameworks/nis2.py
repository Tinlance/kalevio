NIS2_ARTICLE_21_MEASURES = [
    {"id": "a", "title": "Risk Analysis & Security Policies", "article": "21(2)(a)", "weight": 10},
    {"id": "b", "title": "Incident Handling", "article": "21(2)(b)", "weight": 15},
    {"id": "c", "title": "Business Continuity & Crisis Management", "article": "21(2)(c)", "weight": 10},
    {"id": "d", "title": "Supply Chain Security", "article": "21(2)(d)", "weight": 10},
    {"id": "e", "title": "Security in Network & IS Acquisition", "article": "21(2)(e)", "weight": 10},
    {"id": "f", "title": "Effectiveness of Cyber Risk Management", "article": "21(2)(f)", "weight": 10},
    {"id": "g", "title": "Cybersecurity Training & Hygiene", "article": "21(2)(g)", "weight": 8},
    {"id": "h", "title": "Cryptography & Encryption", "article": "21(2)(h)", "weight": 10},
    {"id": "i", "title": "Human Resources Security & Access Control", "article": "21(2)(i)", "weight": 9},
    {"id": "j", "title": "Multi-Factor Authentication", "article": "21(2)(j)", "weight": 8},
]

CSIRT_ENDPOINTS = {
    "EE": {"name": "RIA (Estonia)", "url": "https://www.ria.ee", "email": "cert@cert.ee"},
    "DE": {"name": "BSI (Germany)", "url": "https://www.bsi.bund.de", "email": "nis2@bsi.bund.de"},
    "NL": {"name": "NCSC-NL (Netherlands)", "url": "https://www.ncsc.nl", "email": "nis2@ncsc.nl"},
    "BE": {"name": "CCB (Belgium)", "url": "https://ccb.belgium.be", "email": "cert@cert.be"},
    "FR": {"name": "ANSSI (France)", "url": "https://www.ssi.gouv.fr", "email": "nis2@ssi.gouv.fr"},
    "PL": {"name": "CERT.PL (Poland)", "url": "https://cert.pl", "email": "nis2@cert.pl"},
    "SE": {"name": "NCSC-SE (Sweden)", "url": "https://www.ncsc.se", "email": "nis2@ncsc.se"},
    "IT": {"name": "ACN (Italy)", "url": "https://www.acn.gov.it", "email": "nis2@acn.gov.it"},
    "ES": {"name": "INCIBE (Spain)", "url": "https://www.incibe.es", "email": "nis2@incibe.es"},
    "IE": {"name": "NCSC-IE (Ireland)", "url": "https://www.ncsc.gov.ie", "email": "nis2@ncsc.gov.ie"},
}

def get_csirt(country_code: str) -> dict:
    return CSIRT_ENDPOINTS.get(country_code.upper(), CSIRT_ENDPOINTS["EE"])

def calculate_compliance_score(measures_status: dict) -> int:
    total = sum(m["weight"] for m in NIS2_ARTICLE_21_MEASURES)
    earned = sum(m["weight"] for m in NIS2_ARTICLE_21_MEASURES if measures_status.get(m["id"]) == "compliant")
    return round((earned / total) * 100)
