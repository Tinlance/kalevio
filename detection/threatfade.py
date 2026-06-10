from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class ThreatResult:
    threat_detected: bool; threat_name: str; threat_family: str
    z_score: float; confidence: float; packet_count: int
    mitre_ttps: List[str]; source_ip: Optional[str]; protocol: str; raw_features: dict

KNOWN_THREATS = {
    "merlin_quic":   {"family": "C2", "ttps": ["T1071.001", "T1027", "T1573.001"], "z_threshold": 5.0},
    "cobalt_strike": {"family": "C2", "ttps": ["T1059", "T1055", "T1071.001"], "z_threshold": 4.0},
    "icedid":        {"family": "Banking Trojan", "ttps": ["T1566", "T1204", "T1055"], "z_threshold": 2.5},
    "dns_exfil":     {"family": "Exfiltration", "ttps": ["T1071.004", "T1048"], "z_threshold": 2.5},
}

class ThreatFadeEngine:
    def __init__(self, zscore_threshold: float = 2.5):
        self.zscore_threshold = zscore_threshold

    def analyze_features(self, features: dict) -> ThreatResult:
        sizes = features.get("packet_sizes", [])
        if not sizes:
            return ThreatResult(False, "Clean", "None", 0.0, 0.0, 0, [], None, "unknown", features)
        mean = np.mean(sizes)
        std = np.std(sizes) if len(sizes) > 1 else 0.001
        z = abs((mean - 512) / (std + 0.001))
        detected = z >= self.zscore_threshold
        name, family, ttps = ("Unknown C2", "C2", ["T1071.001", "T1027"]) if detected else ("Clean", "None", [])
        for tname, sig in KNOWN_THREATS.items():
            if z >= sig["z_threshold"] * 2:
                name, family, ttps = tname.replace("_", " ").title(), sig["family"], sig["ttps"]; break
        return ThreatResult(detected, name, family, round(z, 2), min(z/15.0, 1.0),
            len(sizes), ttps, features.get("source_ip"), features.get("protocol", "unknown"), features)

engine = ThreatFadeEngine()
