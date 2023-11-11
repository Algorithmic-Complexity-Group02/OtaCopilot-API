from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT
from ..algorithms.bfs import get_recommended_animes


anime= APIRouter()

@anime.get("/anime{anime_name}")
async def get_anime(anime_name: str):
    get_recommended_animes(anime_name)
