from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import ShowUser, User
from .. import models
from blog.database import get_db
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# db:Session = Depends(get_db) is a db connection


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create(request: User, db: Session = Depends(get_db)):
    newUser = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/get/{id}", response_model=ShowUser)
async def get(id: int, db:Session = Depends(get_db)):
        singleUser = db.query(models.User).filter(models.User.id ==id ).first()

        if not singleUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

        return singleUser