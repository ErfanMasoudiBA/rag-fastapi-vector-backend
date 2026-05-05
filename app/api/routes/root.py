from fastapi import APIRouter
from app.schemas.root import RootResponse
router = APIRouter(tags=["root"])
# this is what uvicorn execute
# the code to run in terminal is:
# uvicorn app.main:app --reload
@router.get("/", response_model=RootResponse)
# whenever some one calls / with GET method, do this def root
# this function is our Handler endpoint
def root():
    return RootResponse(message="FastAPI RAG Docs Assistant is running")
    
# fastapi change this dictionary to json response itself.
