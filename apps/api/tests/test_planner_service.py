from agent_core.policies import ToolPolicyEngine
from agent_core.runtime import AgentRuntime, PlannerExecutionContext


def test_live_conditions_require_approval() -> None:
    runtime = AgentRuntime(ToolPolicyEngine(live_http_enabled=True, approved_hosts=["api.open-meteo.com"]))
    context = PlannerExecutionContext(
        run_id="run_approval",
        mode="offroad",
        request={"title": "Approval flow", "refresh_live_conditions": True},
        trail_catalog=[],
    )
    recommendation, checklist, execution, approval = runtime.execute(context)
    assert approval is not None
    assert approval.required is True
    assert execution.outputs["approval_required"] is True

