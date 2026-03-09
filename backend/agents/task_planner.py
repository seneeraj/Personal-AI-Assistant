from backend.services.llm_service import generate_response


def create_plan(user_goal):

    prompt = f"""
You are an AI planner.

Break the user's goal into clear steps.

Goal:
{user_goal}

Return a numbered plan.
"""

    plan = generate_response(prompt)

    steps = []

    for line in plan.split("\n"):

        if line.strip().startswith(("1", "2", "3", "4", "5")):
            steps.append(line)

    return steps