from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import time
import uuid
from app.api.scenario import router as scenario_router
from app.api.instrument import router as instrument_router
from app.api.portfolio import router as portfolio_router
from app.api.report import router as report_router
from app.api.explain import router as explain_router
from app.api.dialog import router as dialog_router
from app.api.offer_check import router as offer_check_router

app = FastAPI(title='Investment Scenario Lab API', version='1.0.0')
logger = logging.getLogger(__name__)
raw_origins = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()] or ["http://localhost:5173", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.time()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info("request_completed", extra={"request_id": request_id, "method": request.method, "path": request.url.path, "status_code": response.status_code, "duration_ms": round((time.time() - start) * 1000, 2)})
    return response

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled API error", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "code": "internal_error"})

@app.get("/health")
def health():
    return {"status": "ok", "service": "investment-scenario-lab"}

@app.get("/api/health")
def api_health():
    return {"status": "ok", "service": "investment-scenario-lab"}

app.include_router(scenario_router, prefix='/api/scenario', tags=['scenario'])
app.include_router(instrument_router, prefix='/api/instrument', tags=['instrument'])
app.include_router(portfolio_router, prefix='/api/portfolio', tags=['portfolio'])
app.include_router(report_router, prefix='/api/report', tags=['report'])
app.include_router(explain_router, prefix='/api/instruments', tags=['instruments'])

app.include_router(dialog_router, prefix="/api", tags=["dialog"])

app.include_router(offer_check_router, prefix="/api", tags=["offer-check"])
