from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.loaders.model_loader import load_regression_model
from src.models.reg_prediction import reg_predict

@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.reg_model = load_regression_model()
    print("Model loaded, server starting...")
    yield
    print("Server shutting down, cleaning up")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/prediction")
async def prediction(input: dict) -> int:
    prediction = None
    try:
        prediction = reg_predict(app.state.reg_model, input)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return prediction