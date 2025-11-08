from fastapi import APIRouter

health_router = APIRouter(include_in_schema=False)


@health_router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
