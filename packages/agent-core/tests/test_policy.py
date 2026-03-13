from agent_core.policies import ToolPolicyEngine


def test_http_requires_approval_when_enabled() -> None:
    policy = ToolPolicyEngine(live_http_enabled=True, approved_hosts=["api.open-meteo.com"])
    result = policy.evaluate("http", "get", "api.open-meteo.com")
    assert result.decision == "require_approval"

