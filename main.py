import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.auth import router as auth_router
from routes.members import router as members_router
from routes.subscriptions import router as subscriptions_router
from routes.payments import router as payments_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Subscription & Membership Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(members_router)
app.include_router(subscriptions_router)
app.include_router(payments_router)


@app.get("/")
def home():

    logger.info("Application Started Successfully")

    return {
        "message": "Subscription & Membership Management System"
    }
