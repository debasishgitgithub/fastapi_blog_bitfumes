from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog.oauth2 import get_current_user

from .. import models
from blog.database import get_db
from ..schemas import Blog, ShowBlog, User

router = APIRouter(
    # prefix="/items",
    tags=["blog"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# db:Session = Depends(get_db) is a db connection

# get all
# here i use status code for response currect status code 
@router.get("/get", response_model=List[ShowBlog])
async def get(db:Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
    allBlogData = db.query(models.Blog).all()
    if not allBlogData: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not available")
    return allBlogData

# get 
@router.get("/get/{id}", status_code=200, response_model=ShowBlog)
async def get(id:int, db:Session = Depends(get_db) ):
    singleBlog = db.query(models.Blog).filter(models.Blog.id ==id ).first()
    
    if not singleBlog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"details": "blog not found"}
    return singleBlog

# create / save blog
@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create(request: Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(name=request.name, desc= request.desc, user_id = 1)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

# delete 
@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, db:Session = Depends(get_db) ):
    blog  = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():  # Check if the record exists
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} deleted successfully"}

# update blog 
@router.put("/edit/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
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
