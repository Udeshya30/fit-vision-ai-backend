from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ContactRequest
from email_service import send_contact_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/contact")
def contact(data: ContactRequest):
    try:
        send_contact_email(
            name=data.name,
            email=data.email,
            message=data.message,
        )
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email")
