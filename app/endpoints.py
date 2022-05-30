from fastapi import APIRouter


products = {"products": [
    {"item": "bicycle", "qty": 3},
    {"item": "ball", "qty": 4}
]}


router = APIRouter()

@router.get('/get_products')
def get_products():
    return products
        
@router.get('/get_product')
def get_product():
    return {"single_product": {"name":"some_prod325632", "qty":6}}


