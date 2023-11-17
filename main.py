from fastapi import FastAPI, Request, Depends, Response, status, HTTPException, Cookie
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
import pandas as pd
import numpy as np
from OtaCopilotProject.algorithms.bfs import *
from typing import List

app = FastAPI(
    title="OtaCopilot API",
    description="Simple API with FastAPI and CSV files",
    version="0.1.0",
)

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("./templates/index.html")

# Ruta para obtener recomendaciones de animes
@app.get("/api/v1/recommendations/{anime_name}")
async def get_recommendations(anime_name: str):
    recommended_animes = get_recommended_animes(anime_name)

    print(recommended_animes)
    #que devuelva 20 animes
    return recommended_animes

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
