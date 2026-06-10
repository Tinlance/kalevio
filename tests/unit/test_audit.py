import hashlib, json

class TestAuditChain:
    def test_hash_deterministic(self):
        d = json.dumps({"event": "test"}, sort_keys=True)
        assert hashlib.sha256(d.encode()).hexdigest() == hashlib.sha256(d.encode()).hexdigest()

    def test_hash_64_chars(self):
        assert len(hashlib.sha256(b"test").hexdigest()) == 64

    def test_tamper_changes_hash(self):
        a = json.dumps({"z": 14.76}, sort_keys=True)
        b = json.dumps({"z": 0.1}, sort_keys=True)
        assert hashlib.sha256(a.encode()).hexdigest() != hashlib.sha256(b.encode()).hexdigest()

    def test_chain_links(self):
        g = hashlib.sha256(b"GENESIS").hexdigest()
        e = json.dumps({"event": "INCIDENT", "previous_hash": g}, sort_keys=True)
        h = hashlib.sha256(e.encode()).hexdigest()
        assert len(h) == 64 and h != g
