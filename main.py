import json
import pandas
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal


app = FastAPI(title="Revision API")


class CreateProduct(BaseModel):
    id: int = Field(..., description="Product id")
    name: str
    description: str = Field(..., max_length=2000)
    price: int | float
    in_stock: str = Literal[True, False]
    quantity: int
    tag: List[str]

    @field_validator('name')
    @classmethod
    def name_tranfer(cls, value):
        return value.capitalize()

    @model_validator(mode='after')
    def validate_price(cls, value):
        if value.price <= 0:
            raise HTTPException(401, "Price must be greater then 0")



@app.get('/')
def home():
    return {
        'message': 'Welcome to the revision session'
    }


@app.get("/health")
def health():
    return {
        'status': 200,
        'message': 'API is running successfully'
    }

def load_file():
    with open("product.json", 'r') as f:
        return json.load(f)


@app.get('/product')
def product():
    data = load_file()
    return data



@app.get('/product/{id}')
def get_product(id: int = Path(..., description="Enter the id to get sepcific product")):
    product = load_file()

    for item in product:
        if item['id'] == id:
            return item
    raise HTTPException(404, "Product not found")



@app.get('/product')
def get_category(category: str | None = Query(None)):
    product = load_file()
    
    for item in product:
        if item['category'].lower() == category:
            return item
    raise HTTPException(404, "Product not found")



@app.post('/create_product')
def create_product(input: CreateProduct):
    data = pandas.DataFrame({
        'id': input.id,
        'name': input.name,
        'description': input.description,
        'price': input.price,
        'in_stock': input.in_stock,
        'quantity': input.quantity,
        'tag': input.tag
    })
    return data