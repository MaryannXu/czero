# FastAPI is main class used for creating FastAPI applications
# HTTPException is an exception class provided by FastAPI for handling HTTP errors
from fastapi import FastAPI, HTTPException

# imports the BaseModel class from the pydantic module
from pydantic import BaseModel

from typing import Optional

app = FastAPI()

# Python Dictionary data store
inventory = {
    "CZPR": {
        "product_name": "CZero Pen Brand",
        "variant": "Red Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "CZPB": {
        "product_name": "CZero Pen Brand",
        "variant": "Blue Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "CZPG": {
        "product_name": "CZero Pen Brand",
        "variant": "Green Pen",
        "price": 1.00,
        "quantity": 5,
        "description": "High quality pens that are carbon-neutral"
    },
    "RPG": {
        "product_name": "Red’s Pens",
        "variant": "Black Fountain Pen",
        "price": 5.00,
        "quantity": 100,
        "description": "Fountain pens designed by Paul Red"
    },
    "PRG": {
        "product_name": "Red’s Pens",
        "variant": "Purple Fountain Pen",
        "price": 5.00,
        "quantity": 100,
        "description": "Fountain pens designed by Paul Red"
    },
    "BYP": {
        "product_name": "Good Quality Pencil",
        "variant": "",
        "price": 0.50,
        "quantity": 1000,
        "description": "Handmade Pencils"
    }
}

# Models
class Product(BaseModel):
    product_name: str
    variant: Optional[str]
    price: float
    quantity: int
    description: str

# Get all the products and show whole inventory
@app.get("/products")
def get_products():
    return inventory

# Get a specific product by the SKU
@app.get("/products/{sku}")
def get_product(sku: str):
    if sku in inventory:
        return inventory[sku]
    raise HTTPException(status_code=404, detail="Product not found") # 404 http status code = not found

# Add a new product
@app.post("/products")
def add_product(product: Product):
    sku = product.variant.upper().replace(" ", "")
    if sku in inventory:
        raise HTTPException(status_code=400, detail="Product already exists") # 400 http status code = bad request

    # assigning a dictionary representation of the product object to the specified SKU key
    inventory[sku] = product.dict()
    return {"message": "Product added successfully"}

# Update an existing product that is in the inventory
@app.put("/products/{sku}")
def update_product(sku: str, product: Product):
    if sku in inventory:
        inventory[sku] = product.dict()
        return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found") # 404 http status code = not found

# Remove a product that is in the inventory
@app.delete("/products/{sku}")
def remove_product(sku: str):
    if sku in inventory:
        del inventory[sku]
        return {"message": "Product removed successfully"}
    raise HTTPException(status_code=404, detail="Product not found") # 404 http status code = not found

# Buy products and calculate the total price (Shopping Cart)
@app.post("/buy")
def buy_products(products: dict):
    total_price = 0.0
    for sku, quantity in products.items():
        if sku in inventory:
            price = inventory[sku]["price"]
            total_price += price * quantity
        else:
            raise HTTPException(status_code=404, detail=f"Product not found for SKU: {sku}") # 404 http status code = not found
    return {"Total price in shopping cart": total_price}

# Global search all product features across all fields
@app.get("/search/{query}")
def global_search(query: str):
    results = []
    for sku, product in inventory.items():
        for value in product.values():
            if query.lower() in str(value).lower(): # performs a case-insensitive search
                results.append(product) # if match is found, adds product to results list
                break # ensures that each product is only appended to the results list once
    #returns all products that match the query
    return results