from datetime import datetime

def create_user(email: str, password_hash: str, name: str):
    return {
        "email": email,
        "password_hash": password_hash,
        "profile": {
            "name": name,
            "age": None,
            "weight": None,
            "lifestyle": None,
        },
        "onboarding_completed": False,
        "created_at": datetime.utcnow(), 
        "last_login": None,
    }