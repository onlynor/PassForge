import pytest
from generator import (
    generate_password,
    batch_generate,
    password_info,
    calc_entropy,
    ALLOWED_LENGTHS,
    UPPERCASE,
    LOWERCASE,
    DIGITS,
    SPECIAL,
)


class TestStandardPassword:
    def test_generates_correct_length(self):
        for length in ALLOWED_LENGTHS:
            pw = generate_password(length)
            assert len(pw) == length

    def test_contains_all_categories(self):
        pw = generate_password(32)
        assert any(c in UPPERCASE for c in pw)
        assert any(c in LOWERCASE for c in pw)
        assert any(c in DIGITS for c in pw)
        assert any(c in SPECIAL for c in pw)

    def test_invalid_length_raises(self):
        with pytest.raises(ValueError):
            generate_password(10)

    def test_batch_generate_count(self):
        passwords = batch_generate(16, 5)
        assert len(passwords) == 5


class TestEntropyCalculation:
    def test_standard_entropy(self):
        pw = generate_password(16)
        entropy = calc_entropy(pw)
        assert entropy > 0

    def test_longer_password_higher_entropy(self):
        short = generate_password(8)
        long_pw = generate_password(32)
        assert calc_entropy(long_pw) > calc_entropy(short)


class TestPasswordInfo:
    def test_standard_info(self):
        pw = generate_password(16)
        info = password_info(pw)
        assert "password" in info
        assert "length" in info
        assert "entropy" in info
        assert "strength" in info
        assert info["length"] == 16


class TestAPIEndpoints:
    def test_config_endpoint(self):
        from app import app
        client = app.test_client()

        resp = client.get('/api/config')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'allowedLengths' in data
        assert 'maxLength' in data
        assert 'maxCount' in data

    def test_generate_standard(self):
        from app import app
        client = app.test_client()

        resp = client.post('/api/generate', json={"length": 16, "count": 1})
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["passwords"]) == 1

    def test_count_range_validation(self):
        from app import app
        client = app.test_client()

        resp = client.post('/api/generate', json={"length": 16, "count": 0})
        assert resp.status_code == 400

        resp = client.post('/api/generate', json={"length": 16, "count": 501})
        assert resp.status_code == 400

        resp = client.post('/api/generate', json={"length": 16, "count": 1})
        assert resp.status_code == 200

    def test_invalid_length_rejected(self):
        from app import app
        client = app.test_client()

        resp = client.post('/api/generate', json={"length": 10, "count": 1})
        assert resp.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
