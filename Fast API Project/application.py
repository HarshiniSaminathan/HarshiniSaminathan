from fastapi import FastAPI
from app.config import create_tables
from app.views import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    await create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5005, reload=True)
