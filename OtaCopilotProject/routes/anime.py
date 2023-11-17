from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT
from ..algorithms.bfs import get_recommended_animes


anime = APIRouter()

## @anime.get("/animes/{anime_name}")
## async def get_anime(anime_name: str):
##     list_animes_recommended = get_recommended_animes(anime_name)
##     list_animes_recommended.to_dict(orient='records')
##     return list_animes_recommended


