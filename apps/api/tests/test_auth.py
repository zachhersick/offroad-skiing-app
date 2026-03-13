from app.core.security import decode_token


def test_access_token_round_trip() -> None:
    from app.core.security import create_access_token

    token = create_access_token("user_123")
    payload = decode_token(token)
    assert payload["sub"] == "user_123"
    assert payload["type"] == "access"

