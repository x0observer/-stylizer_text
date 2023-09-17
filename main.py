
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine import engine, init_db
from sqlmodel import SQLModel

from middleware.scraping.service import router as scraping_router
from middleware.intelegens.service import router as intelegens_router

from src.stock.service import router as stock_router
from src.profile.service import router as profile_router
app = FastAPI(debug=True)

@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(scraping_router, prefix="/middleware")
app.include_router(stock_router, prefix="/stock")
app.include_router(profile_router, prefix="/profile")
app.include_router(intelegens_router, prefix="/intelegense")

origins = ["*"]


# def catch_exceptions_middleware(request: Request, call_next):
#     try:
#         return call_next(request)
#     except Exception as err:
#         return Response("Internal server error", status_code=500)


# app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# def create_and_fill_database():
#     # SQLModel.metadata.drop_all(engine)
#     SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, timeout_keep_alive=600)
