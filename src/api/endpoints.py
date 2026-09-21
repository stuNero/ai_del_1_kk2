from fastapi import FastAPI, HTTPException

from src.loaders.model_loader import load_regression_model
from src.models.reg_prediction import reg_predict

model = load_regression_model()

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/prediction")
async def prediction(input: dict) -> int:
    prediction = None
    try:
        prediction = reg_predict(model, input)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return prediction