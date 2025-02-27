from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import Token
from .. import models, token
from blog.database import get_db
from ..hashing import Hash


router = APIRouter(
    # prefix="/authenticate",
    tags=["authenticate"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.email==request.username ).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"details": "blog not found"}
        
    if not Hash.verify(request.password, user.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Password not match")

    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    # return {"access_token":access_token, "token_type":"bearer"}
    return Token(access_token=access_token, token_type="bearer")