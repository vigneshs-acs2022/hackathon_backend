from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from survey.api import survey_router

app = FastAPI()

if (os.environ.get('ENVIRONMENT', 'production') == 'production'):
    openapi_url = "/api/openapi.json"
    root_path = "/api"
else:
    openapi_url = "/openapi.json"
    root_path = ""

app = FastAPI(docs_url="/docs", openapi_url=openapi_url, root_path=root_path, title="Survey APIs", description="This is a Suervey API",
              swagger_ui_parameters={"defaultModelsExpandDepth": -1, "tryItOutEnabled": True, "docExpansion": "none"})


# CORS middleware
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(survey_router,
                   prefix="/survey", tags=["survey"])