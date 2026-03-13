from agent_core.policies import ToolPolicyEngine
from agent_core.runtime import AgentRuntime, PlannerExecutionContext


def test_ski_runtime_picks_wider_ski_for_powder() -> None:
    runtime = AgentRuntime(ToolPolicyEngine(live_http_enabled=False))
    context = PlannerExecutionContext(
        run_id="ski_run",
        mode="ski",
        request={"title": "Storm day", "refresh_live_conditions": False},
        profile={"snow_preference": "powder", "preferred_terrain": "all_mountain"},
        ski_quiver={
            "skis": [
                {"name": "Daily Driver 98", "waist_mm": 98, "terrain_bias": "all_mountain"},
                {"name": "Storm Board 112", "waist_mm": 112, "terrain_bias": "all_mountain"},
            ]
        },
    )
    recommendation, checklist, _, _ = runtime.execute(context)
    assert recommendation.ranked_options[0].title == "Storm Board 112"
    assert any(item.category == "snow" for item in checklist.items)
