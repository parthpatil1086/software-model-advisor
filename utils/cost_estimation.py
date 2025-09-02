def estimate_cost(input_data):
    """
    Estimates project development cost based on input factors.

    Parameters:
        input_data (dict): A dictionary containing client input.

    Returns:
        int: Estimated cost in INR.
    """

    base_cost = 20000  # Starting base cost

    # Domain multiplier
    domain_multiplier = {
        "Web App": 1.2,
        "Mobile App": 1.4,
        "AI Tool": 1.6,
        "Enterprise Software": 1.8,
        "Other": 1.0
    }

    # Duration multiplier
    duration_multiplier = {
        "<1 month": 1.0,
        "1–3 months": 1.5,
        "3–6 months": 2.0,
        ">6 months": 2.5
    }

    # Team size cost
    team_size_cost = input_data.get("team_size", 5) * 5000

    domain = input_data.get("domain")
    duration = input_data.get("duration")

    cost = base_cost
    cost *= domain_multiplier.get(domain, 1.0)
    cost *= duration_multiplier.get(duration, 1.0)
    cost += team_size_cost

    # Add urgency cost if deadline is strict
    if input_data.get("deadline") == "Yes":
        cost += 10000

    return int(cost)