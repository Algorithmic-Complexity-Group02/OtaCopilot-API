from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np

app = FastAPI(
    title="OtaCopilot API",
    description="Simple API with FastAPI and CSV files",
    version="0.1.0",
)

@app.get("/")
async def root():
    return FileResponse("./templates/index.html")

@app.get("/api/v1/animes")
async def get_animes():
    df = pd.read_csv("OtaCopilotProject/static/animeTest.csv")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(1)
    return df.to_dict(orient='records')

@app.get("/api/v1/users")
async def get_users():
    df = pd.read_csv("OtaCopilotProject/static/profileTest.csv").T.to_dict()
    return df


@app.get("/api/v1/animes/{anime_name}")
async def get_anime_by_name(anime_name: str):
    df = pd.read_csv("OtaCopilotProject/static/animeTest.csv")
    df = df[df["name"] == anime_name]

    if df.empty:
        raise HTTPException(status_code=404, detail="Anime not found")

    return df.iloc[0].to_dict()
