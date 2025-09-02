def suggest_model(input_data):
    """
    Suggests a software development model based on project input.

    Parameters:
        input_data (dict): A dictionary containing client input.

    Returns:
        str: Suggested development model name.
    """

    domain = input_data.get("domain")
    team_size = input_data.get("team_size")
    duration = input_data.get("duration")
    deadline = input_data.get("deadline")
    budget = input_data.get("budget")

    # Rule-based model suggestion (basic logic for now)
    if domain == "Enterprise Software" or team_size > 10:
        return "Spiral Model"
    elif deadline == "Yes" and duration == "<1 month":
        return "Waterfall Model"
    elif domain == "Web App" or domain == "Mobile App":
        return "Agile Model"
    elif budget == "<50K":
        return "Rapid Application Development (RAD)"
    else:
        return "Incremental Model"