from fastapi import FastAPI
from router import api_router

# Create a FastAPI instance
app = FastAPI()

# Include the API router
app.include_router(api_router)


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"health": "Good"}
