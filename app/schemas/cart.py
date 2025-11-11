from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductResponse # Necesitamos el esquema de Product

# Esquema para el ítem dentro del carrito
class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(CartItemBase):
    pass
    
# Esquema de respuesta para un ítem del carrito (incluye detalles del producto)
class CartItemResponse(CartItemBase):
    # Incluimos el modelo de respuesta del producto completo para el detalle del carrito
    product: ProductResponse
    
    class Config:
        from_attributes = True

# Esquema de respuesta para el Carrito completo
class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    
    class Config:
        from_attributes = True
