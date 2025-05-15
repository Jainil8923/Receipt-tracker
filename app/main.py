from services.auth_service import auth_router
from api.routes.receipt_route import receipt_router
from api.routes.user_route import user_router
from api.routes.ocr_receipt_route import ocr_receipt_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(receipt_router, prefix='/receipts')
app.include_router(user_router, prefix='/user')
app.include_router(ocr_receipt_router, prefix='/OCR')