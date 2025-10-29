
import joblib
import numpy as np

def suggest_model(client_input):
    """Predicts best software model using trained ML model"""
    try:
        model = joblib.load("ml_models/model_suggestion.pkl")
        
        features = np.array([
            len(client_input["goal"]),
            client_input["team_size"],
            {"Low": 1, "Medium": 2, "High": 3}.get(client_input["complexity"], 2)
        ]).reshape(1, -1)
        prediction = model.predict(features)
        return prediction[0]
    except:
        if client_input["complexity"] == "High" or client_input["risk"] == "High":
            return "Spiral Model"
        elif client_input["involvement"] == "Active":
            return "Agile Model"
        elif client_input["deadline"] == "Yes":
            return "Waterfall Model"
        else:
            return "Iterative Model"
