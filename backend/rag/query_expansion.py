def expand_query(query: str):

    q = query.lower()

    expansions = [query]

    if "capstone" in q:
        expansions.extend([
            "capstone project start date",
            "capstone project timeline",
            "capstone project duration"
        ])

    if "exam" in q:
        expansions.extend([
            "exam schedule",
            "exam duration",
            "exam timing"
        ])

    if "appointment" in q:
        expansions.extend([
            "independent director appointment",
            "board appointment rules"
        ])

    return list(set(expansions))