from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }

# this is what uvicorn execute
# the code to run in terminal is:
# uvicorn app.main:app --reload
@router.get("/")
# whenever some one calls / with GET method, do this def root
# this function is our Handler endpoint
def root():
    return{
        "message": "FastAPI RAG Docs Assistant is running"
    }
    
# fastapi change this dictionary to json response itself.
