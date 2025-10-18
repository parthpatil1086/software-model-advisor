def optimize_budget(estimated_cost, budget_range):
    """Compares estimated cost vs selected budget and gives suggestions"""
    ranges = {"<50K": 50000, "50K–1L": 100000, "1L–5L": 500000, ">5L": 1000000, ">10L": 10000000}
    max_budget = ranges.get(budget_range, 0)

    if estimated_cost <= max_budget:
        return {"within_budget": True, "message": "✅ Project fits within your budget!", "suggestions": []}
    else:
        diff = estimated_cost - max_budget
        suggestions = [
            "Use open-source or free tools",
            "Reduce project scope or non-critical features",
            "Optimize team size or project duration",
            "Consider milestone-based payments"
        ]
        return {"within_budget": False, "message": f"⚠️ Over budget by ₹{diff}", "suggestions": suggestions}
