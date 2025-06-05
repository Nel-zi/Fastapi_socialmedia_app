from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from ..import models, database, schemas, utils, oauth2

router = APIRouter(
    tags=['Authentication']
    )

# The OAuth2PasswordRequestForm import means that we don't need a login schema anymore, it handles it as a form. 
# Remember OAuth2PasswordRequestForm doesn't specify email, it instead displays it as username but you can still go with email.
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #OAuth2PasswordRequestForm made us change it from ".email" to ".username"

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credantials")
    

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credantials")
    
    access_token = oauth2.create_access_token(data = {"userID": user.user_id})

    return {"access_token": access_token,
            "token_type": "bearer"
            }