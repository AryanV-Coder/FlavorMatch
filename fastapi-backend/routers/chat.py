from fastapi import APIRouter, HTTPException
from 

router = APIRouter()

@router.post("/chat")
async def chat()