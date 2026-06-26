from fastapi import APIRouter

router = APIRouter()


@router.get("/system")
async def system():
    return {"message": "System endpoint - not yet implemented"}
