from fastapi import FastAPI, Depends, status
from .schemas import Blog
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# for migrate models to database 
models.Base.metadata.create_all(engine)

# db:Session = Depends(get_db) is a db connection

# here i use status code for response currect status code 
@app.post("/create",status_code=status.HTTP_201_CREATED)
async def create(request: Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(name=request.name, desc= request.desc)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

@app.get("/get")
async def get(db:Session = Depends(get_db)):
    allBlogData = db.query(models.Blog).all()
    return allBlogData

@app.get("/get/{id}")
async def get(id:int, db:Session = Depends(get_db)):
    return db.query(models.Blog).filter(models.Blog.id ==id ).first()