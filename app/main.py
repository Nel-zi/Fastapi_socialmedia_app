from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, likes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# this links all the router files to the main.py file
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)



@app.get("/")
def root():
    return {"message": "Hello World1"}


if __name__ == "__main__":
    # Use PORT environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    # Bind to 0.0.0.0 so Render can forward external traffic
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)






