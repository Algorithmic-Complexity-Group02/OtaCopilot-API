from fastapi import FastAPI, Request, Depends, Response, status, HTTPException, Cookie
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
import uvicorn 
import pandas as pd

app = FastAPI(
    title="OtaCopilot API",
    description="Simple API to with FasAPI and CSV files",
    version="0.1.0",
)

@app.get("/")
async def root():
    return FileResponse("./templates/index.html")

@app.get("/api/v1/animes")
async def get_animes():
    df = pd.read_csv("OtaCopilotProject/static/animeTest.csv").T.to_dict()
    return df

@app.get("/api/v1/users")
async def get_users():
    df = pd.read_csv("OtaCopilotProject/static/profileTest.csv").T.to_dict()
    return df

@app.get("/api/v1/animes/{anime_name}")
async def get_anime_by_name(anime_name: str):
    df = pd.read_csv("OtaCopilotProject/static/animeTest.csv")
    df = df[df["name"] == anime_name]
    return df.to_dict()