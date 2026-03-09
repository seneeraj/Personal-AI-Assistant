from backend.agents.task_planner import create_plan
from backend.agents.task_executor import execute_step


def autonomous_agent(user_goal, document=None):

    plan = create_plan(user_goal)

    results = []

    for step in plan:

        result = execute_step(step, user_goal, document)

        results.append({
            "step": step,
            "result": result
        })

    return results