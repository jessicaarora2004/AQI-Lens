from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow frontend to fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Delhi Pollution ML API is running"}

@app.get("/predict")
def predict():
    df = pd.read_csv("delhi_zones.csv")
    return df.to_dict(orient="records")

@app.post("/get_zone_info")
async def get_zone_info(req: Request):
    data = await req.json()
    zone_id = data.get("zone_id")
    df = pd.read_csv("delhi_zones.csv")
    filtered = df[df['zone'] == zone_id]

    if filtered.empty:
        return {
            "zone_id": zone_id,
            "pm25": 0,
            "primary_source": "Unknown",
            "recommendation": "Zone not found in database."
        }

    row = filtered.iloc[0]

    score = round(
        0.35*row["night_light"] +
        0.25*row["industry"] +
        0.2*row["traffic"] +
        0.15*row["dust"] +
        0.05*row["biomass"], 2
    ) * 500

    if score > 300:
        recommendation = "Very unhealthy. Avoid outdoor activity. Wear N95 mask."
    elif score > 200:
        recommendation = "Unhealthy. Reduce outdoor exposure."
    elif score > 100:
        recommendation = "Moderate air quality. Sensitive groups take care."
    else:
        recommendation = "Air quality is acceptable."

    primary_source = "Traffic & Industry" if score>150 else "Residential / Dust"

    return {
        "zone_id": zone_id,
        "pm25": score,
        "primary_source": primary_source,
        "recommendation": recommendation
    }
