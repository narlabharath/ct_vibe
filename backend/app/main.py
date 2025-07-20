
from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="File-Based Chat System API",
    description="Backend for file-based chat system. More routers will be included later.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the File-Based Chat System API!"}

# More routers will be included here later

app.include_router(api_router)
