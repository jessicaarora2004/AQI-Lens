import numpy as np
import pandas as pd

def compute_pollution_score(row):
    score = (
        0.35 * row["night_light"] +
        0.25 * row["industry"] +
        0.20 * row["traffic"] +
        0.15 * row["dust"] +
        0.05 * row["biomass"]
    )
    return round(score * 500, 2)

def generate_recommendation(score):
    if score > 300:
        return "Very unhealthy. Avoid outdoor activity. Wear N95 mask."
    elif score > 200:
        return "Unhealthy. Reduce outdoor exposure."
    elif score > 100:
        return "Moderate air quality. Sensitive groups take care."
    else:
        return "Air quality is acceptable."

def predict_all(df):
    results = []
    for _, row in df.iterrows():
        score = compute_pollution_score(row)
        results.append({
            "zone": row["zone"],
            "lat": row["lat"],
            "lon": row["lon"],
            "aqi": score,
            "recommendation": generate_recommendation(score)
        })
    return results
