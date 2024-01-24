from fastapi import APIRouter,Request,Response,Depends
from survey.crud import Survey
from sqlalchemy.orm import Session
from .models import get_db

survey_router = APIRouter()


@survey_router.post("/user")
async def add_user(data: dict, response: Response, db:Session=Depends(get_db)):
    return {"message":"Hello World"}

@survey_router.get("/languages")
async def add_user(db:Session=Depends(get_db)):
    languages = await Survey.list_languages(db)
    return languages
