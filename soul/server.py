from fastapi import FastAPI
from main import gen_summary
from pydantic import BaseModel
app = FastAPI()

class url_type(BaseModel):
    url:str

#cors policy allow all
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/summary")
def read_summary(data:url_type):

    return {"summary": gen_summary(data.url)}