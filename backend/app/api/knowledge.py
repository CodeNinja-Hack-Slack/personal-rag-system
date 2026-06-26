from fastapi import APIRouter

router = APIRouter()


@router.get("/knowledge")
async def knowledge():
    return {"message": "Knowledge endpoint - not yet implemented"}
