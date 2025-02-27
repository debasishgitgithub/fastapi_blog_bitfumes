from fastapi import FastAPI
from . import models
from .database import engine

from .routers import blog, user, authenticate

app = FastAPI()
app.include_router(blog.router)
app.include_router(authenticate.router)
app.include_router(user.router)

        
# for migrate models to database 
models.Base.metadata.create_all(engine)

# db:Session = Depends(get_db) is a db connection
