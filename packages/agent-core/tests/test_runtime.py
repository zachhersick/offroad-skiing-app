from agent_core.policies import ToolPolicyEngine
from agent_core.runtime import AgentRuntime, PlannerExecutionContext


def test_offroad_runtime_returns_ranked_recommendations() -> None:
    runtime = AgentRuntime(ToolPolicyEngine(live_http_enabled=False))
    context = PlannerExecutionContext(
        run_id="run_1",
        mode="offroad",
        request={"title": "Half day trail run", "refresh_live_conditions": False},
        profile={"preferred_terrain": ["desert"], "comfort_rating": 3, "max_drive_time_hours": 4},
        vehicle={"drivetrain": "4wd", "lift_inches": 1.5, "tire_size_inches": 33, "recovery_gear": {"traction_boards": False}},
        trail_catalog=[
            {"name": "Otay Backbone", "summary": "Rugged scenic route", "terrain": "desert", "difficulty_score": 3, "drive_time_hours": 2, "risks": ["Loose rock"]},
            {"name": "Easy Wash", "summary": "Beginner route", "terrain": "forest", "difficulty_score": 1, "drive_time_hours": 1, "risks": []},
        ],
    )
    recommendation, checklist, execution, approval = runtime.execute(context)
    review = runtime.review(context, recommendation, checklist)
    assert approval is None
    assert recommendation.ranked_options[0].title == "Otay Backbone"
    assert any(item.category == "recovery" for item in checklist.items)
    assert execution.outputs["top_option"] == "Otay Backbone"
    assert review.passed is True

