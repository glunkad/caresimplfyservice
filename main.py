from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import app as api_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
# app.include_router(api_router)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Care Simplify! I'm Natasha, and I'm here to make your experience easier and better. Let's simplify care together!"}
