from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.scenario import router as scenario_router
from app.api.instrument import router as instrument_router
from app.api.portfolio import router as portfolio_router
from app.api.report import router as report_router
from app.api.explain import router as explain_router

app = FastAPI(title='Investment Scenario Lab API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(scenario_router, prefix='/api/scenario', tags=['scenario'])
app.include_router(instrument_router, prefix='/api/instrument', tags=['instrument'])
app.include_router(portfolio_router, prefix='/api/portfolio', tags=['portfolio'])
app.include_router(report_router, prefix='/api/report', tags=['report'])
app.include_router(explain_router, prefix='/api/instruments', tags=['instruments'])
