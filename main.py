from fastapi import FastAPI, Request, Depends, Response, status, HTTPException, Cookie
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from OtaCopilotProject.algorithms.bfs import *
from typing import List
import json
from fastapi import Query

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
    df = df[df["title"] == anime_name]

    if df.empty:
        raise HTTPException(status_code=404, detail="Anime not found")

    anime_data = df.iloc[0].to_dict()

    recommended_anime_ids = get_recommended_animes(anime_name)
    #print(recommended_anime_ids)
    
    recommended_animes_data = []

    for anime_uid, _ in recommended_anime_ids[:19]:
        anime_data = G_nx.nodes[anime_uid]['data']
       # print(anime_data)
        anime_dict = anime_data.to_dict()
       # print(anime_dict)
        
        anime_dict = handle_float_values(anime_dict)  # Manejar valores de punto flotante problemáticos

        recommended_animes_data.append(anime_dict)

    return {"recommended_animes": recommended_animes_data}

@app.get("/api/v1/search/animes")
async def search_animes_by_title(query: str = Query(..., title="Search Term")):
    df = pd.read_csv("OtaCopilotProject/static/animeTest.csv")
    
    filtered_animes = df[df["title"].str.contains(query, case=False)]

    if filtered_animes.empty:
        raise HTTPException(status_code=404, detail="No animes found for the given search term")

    # Convertir los datos de los animes filtrados a un formato JSON
    filtered_animes_data = filtered_animes.to_dict(orient='records')
    return {"search_results": filtered_animes_data}