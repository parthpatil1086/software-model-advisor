
import joblib
import numpy as np

def estimate_cost(client_input):
    """Estimates project cost using ML model or fallback formula"""
    try:
        model = joblib.load("ml_models/cost_estimator.pkl")
        features = np.array([
            client_input["team_size"],
            {"Low": 1, "Medium": 2, "High": 3}.get(client_input["complexity"], 2),
            {"Beginner": 1, "Intermediate": 2, "Expert": 3}.get(client_input["experience"], 2)
        ]).reshape(1, -1)
        return round(model.predict(features)[0])
    except:

        base = 20000
        complexity = {"Low": 1, "Medium": 1.5, "High": 2}.get(client_input["complexity"], 1)
        team_factor = client_input["team_size"] * 3000
        duration_factor = {"<1 month": 1, "1–3 months": 1.5, "3–6 months": 2, ">6 months": 3}.get(client_input["duration"], 1)
        return int(base * complexity + team_factor * duration_factor)
