from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router
from app.api.routes.docs import router as docs_router
from app.api.routes import docs, ingestion
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.vector_store import router as vector_store_router
from app.api.routes.embedding import router as embedding_router
from app.api.routes.retrieval import router as retrieval_router
from app.api.routes.documents import router as documents_router
from app.api.routes.rag import router as rag_router

api_router = APIRouter()
# this router plays the role of router aggregator
# it doesn't define any endpoints, it just gathered other routes

api_router.include_router(root_router)
api_router.include_router(health_router)
api_router.include_router(docs_router)
api_router.include_router(docs.router)
api_router.include_router(ingestion.router)
api_router.include_router(ingestion_router)
api_router.include_router(vector_store_router)
api_router.include_router(embedding_router)
api_router.include_router(retrieval_router)
api_router.include_router(documents_router)
api_router.include_router(rag_router)