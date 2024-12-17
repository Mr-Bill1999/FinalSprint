from fastapi import FastAPI
import joblib
from model import PredictionRequest

app = FastAPI()
model = joblib.load("trained_stacking_model.joblib")

@app.post("/predict/")
async def predict(data: PredictionRequest):
    # Собираем признаки в том же порядке, что при обучении
    input_row = [[
        data.id,
        data.Air_temperature_K,
        data.Process_temperature_K,
        data.Rotational_speed_rpm,
        data.Torque_Nm,
        data.Tool_wear_min,
        data.TWF,
        data.HDF,
        data.PWF,
        data.OSF,
        data.RNF,
        data.Type_H,
        data.Type_L,
        data.Type_M
    ]]
    prediction = model.predict(input_row)
    return {"prediction": prediction.tolist()}
