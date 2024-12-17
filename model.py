from pydantic import BaseModel

class PredictionRequest(BaseModel):
    id: int
    Air_temperature_K: float
    Process_temperature_K: float
    Rotational_speed_rpm: int
    Torque_Nm: float
    Tool_wear_min: int
    TWF: int
    HDF: int
    PWF: int
    OSF: int
    RNF: int
    Type_H: int
    Type_L: int
    Type_M: int
