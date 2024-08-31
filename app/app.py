from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, Response, Cookie 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from bot.database import requests as rq

import os
import dotenv

dotenv.load_dotenv()


app = FastAPI()
templates = Jinja2Templates(directory="app/web/templates")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=f"{os.getenv('SECRET_KEY')}")



@app.get("/", response_class=HTMLResponse)
async def loading_page(request: Request) -> None:
    return templates.TemplateResponse("loading.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request) -> None:
    user_id = request.session.get("user_id")
    try:
        user = await rq.get_user_by_tg_id(user_id)

        return templates.TemplateResponse("home.html", {"request": request, "score": user.score})
    except: 
        return "<h1>Пожалуйста, запустите в боте: @ncrypto_tap_bot</h1>"


@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page(request: Request) -> None:
    users_list = await rq.get_top_100_users()

    return templates.TemplateResponse("leaderboard.html", {"request": request, "users": users_list})


@app.get("/boosts", response_class=HTMLResponse)
async def boosts_page(request: Request):
    return templates.TemplateResponse("soon.html", {"request": request})


@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    return templates.TemplateResponse("soon.html", {"request": request})


@app.get("/friends", response_class=HTMLResponse)
async def friends_page(request: Request):
    user_id = request.session.get("user_id")
    user = await rq.get_user_by_tg_id(user_id)

    referrals = []
    for ref_id in user.referrals:
        if ref_id is not None:
            referral = await rq.get_user_by_tg_id(ref_id)
            referrals.append([referral.name, referral.score])

    return templates.TemplateResponse("friends.html", {"request": request, "referrals": referrals, "user_id": user.tg_id if user else None})


@app.post("/reg")
async def id(request: Request, data: dict) -> None:
    request.session["user_id"] = data["id"]


@app.post("/score")
async def score(request: Request, data: dict = {"id": 0, "score": 0}) -> None:
    await rq.update_user_score(data["id"], data["score"])
