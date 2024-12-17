from fastapi import FastAPI
import joblib
from model import PredictionRequest

app = FastAPI()
model = joblib.load("trained_stacking_model.joblib")

@app.get("/")
async def read_root():
    return {'Великолепная семерка API'}


@app.post("/predict/")
async def predict(data: PredictionRequest):
    input_data = [[data.feature1, data.feature2, data.feature3,data.feature4,data.feature5,
                   data.feature6, data.feature7, data.feature8, data.feature9, data.feature9,
                   data.feature10,data.feature11, data.feature12, data.feature13]]
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}