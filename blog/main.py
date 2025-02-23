from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from .schemas import Blog, ShowBlog, User, ShowUser
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import user


app = FastAPI()
app.include_router(user.router)

        
# for migrate models to database 
models.Base.metadata.create_all(engine)

# db:Session = Depends(get_db) is a db connection



# update blog 
@app.put("/edit/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
async def update(id:int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()  # Retrieve the blog
    
    if not blog:  # Check if the record exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    db.query(models.Blog).filter(models.Blog.id == id).update({
        "name": request.name,
        "desc": request.desc
    }, synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} updated successfully"}    

@app.post("/user/create", status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['user'])
async def create(request: User, db: Session = Depends(get_db)):
    newUser = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@app.get("/user/get/{id}", response_model=ShowUser, tags=['user'])
async def get(id: int, db:Session = Depends(get_db)):
        singleUser = db.query(models.User).filter(models.User.id ==id ).first()

        if not singleUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

        return singleUser