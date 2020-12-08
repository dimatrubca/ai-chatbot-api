from fastapi import APIRouter

router = APIRouter()

@router.post("/test")
def test_route():
    return {'Hello': 'World'}