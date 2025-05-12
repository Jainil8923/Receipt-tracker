from services.auth_service import auth_router
from api.routes.protected import router
from api.routes.receipt_route import receipt_router
from fastapi import FastAPI
from core.security import decode_access_token

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(router, prefix='/protected')
app.include_router(receipt_router, prefix='/receipts')

@app.get("/")
async def root():
    return {"message": "Welcome to the Receipt Tracker API"}