from fastapi import FastAPI
from services.auth_service import auth_router
app = FastAPI()
    
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello World"}