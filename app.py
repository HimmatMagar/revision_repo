from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator, computed_field, Field
from typing import List, Optional, Annotated
from contextlib import asynccontextmanager

class PredictRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=5, max_length=200)]
    age: int = Field(..., description="Age of the person")
    weight: float | int
    height: float | int
    features: Optional[List[float]]

    @field_validator("age")
    def validate_age(cls, value):
        if value < 0 or value > 80:
            raise ValueError("Age must be between 0 and 80")

    @computed_field
    @property
    def bmi(self) -> float:
        return self.height / self.weight

class Response(BaseModel):
    answer: str
    source: List[str]

@asynccontextmanager
async def lifespan(app: FastAPI):
    model = joblib.load("model.pkl")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict", response_model=Response, tags=['inference'])
def post(request: PredictRequest):
    result = model.predict(request[0])
    return result