from fastapi import APIRouter,Request,Response,Depends
from survey.crud import Survey
from sqlalchemy.orm import Session
from .models import get_db

survey_router = APIRouter()


@survey_router.post("/user")
async def add_user(request: Request, response: Response, db:Session=Depends(get_db)):

    add_user = Survey.add_user(
       request, response, db)
    return add_user
