import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import Base, engine
from .router import post, user, auth, vote
from .config import settings

print(settings)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins=["https://www.google.com"]
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time ()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     print(process_time)
#     return response

