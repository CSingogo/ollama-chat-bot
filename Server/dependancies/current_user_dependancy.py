from fastapi import Depends, Request, HTTPException, status
from utils.security import decode_access_token
from models.user_model import UserObject

def get_current_user(request: Request) -> UserObject:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = decode_access_token(token)

    return UserObject(
        id=payload["sub"],
        username=payload["username"],
        account_status=payload["account_status"],
        subscription_plan=payload["subscription_plan"],
        isFirstprompt=payload["isFirstPrompt"]
    )
