def optimize_budget(estimated_cost, budget_input):
    """
    Compares estimated cost with client's budget and suggests optimization tips.

    Parameters:
        estimated_cost (int): The calculated cost of the project.
        budget_input (str): Budget entered by user (e.g., "<50K", "50K–1L", ">1L").

    Returns:
        dict: Result of comparison and suggestions if needed.
    """

    # Convert budget_input to numeric range
    if budget_input == "<50K":
        max_budget = 50000
    elif budget_input == "50K–1L":
        max_budget = 100000
    elif budget_input == ">1L":
        max_budget = 200000  # Assume soft cap
    else:
        max_budget = 0

    # Compare
    if estimated_cost <= max_budget:
        return {
            "within_budget": True,
            "message": f"The estimated cost ₹{estimated_cost} is within the budget range.",
            "suggestions": []
        }
    else:
        # Suggest optimization tips
        suggestions = [
            "Reduce project scope for MVP version.",
            "Choose open-source tools and libraries.",
            "Decrease team size or duration.",
            "Avoid urgent deadlines to reduce costs.",
            "Split the project into phases."
        ]

        return {
            "within_budget": False,
            "message": f"The estimated cost ₹{estimated_cost} exceeds the budget limit of ₹{max_budget}.",
            "suggestions": suggestions
        }