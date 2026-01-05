from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ContactRequest
from app.email_service import send_contact_email
from app.auth.routes import router as auth_router

from app.dashboard import router as dashboard_router
from app.users.routes import router as users_router



app = FastAPI(title="FitVisionAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.0.112:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(users_router)


@app.post("/api/contact")
def contact(data: ContactRequest):
    try:
        send_contact_email(data.name, data.email, data.message)
        return {"success": True}
    except Exception:
        raise HTTPException(status_code=500, detail="Email failed")

@app.get("/")
def root():
    return {"status": "FitVisionAI backend running"}
