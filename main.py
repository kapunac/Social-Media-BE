from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routers import post, user, auth, vote
from config import settings




# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


















# using psycopg to connect to db
# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try: 
#         conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres', password= '26230', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print('db connected')
#         break
#     except Exception as error:
#         print(error)
#         time.sleep(3)
