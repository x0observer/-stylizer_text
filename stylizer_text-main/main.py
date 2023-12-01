
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine import engine, init_db
from sqlmodel import SQLModel

from middleware.scraping.service import router as scraping_router
from middleware.intelegens.service import router as intelegens_router

from src.stock.service import router as stock_router
from src.payment.router import router as payment_router
from src.client.router import router as client_router
from src.profile.service import router as profile_router
from src.auth.v2.router import router as register_router
from src.referral.router import router as referral_router
from middleware.v2.scheduler import router as scheduler_router

# from middleware.scraping.scheduler import scheduler
from middleware.v2.scheduler import SchedulerRepository


app = FastAPI(debug=True)
scheduler = SchedulerRepository()


@app.on_event("startup")
async def startup():
    await init_db()
    
    scheduler.add_job(scheduler.scraping_scheduler, 'interval', minutes=10)
    scheduler.start()



@app.on_event("shutdown")
async def shutdown():
    # Stop the scheduler when the FastAPI app is stopped
    # scheduler.shutdown()
    return 1

app.include_router(referral_router, prefix="/referral")
app.include_router(scheduler_router, prefix="/scheduler")
app.include_router(payment_router, prefix="/payment")
app.include_router(client_router, prefix="/client")
app.include_router(register_router, prefix="/register")
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

    uvicorn.run(app, host="0.0.0.0", port=8000,
                reload=False, timeout_keep_alive=600)
