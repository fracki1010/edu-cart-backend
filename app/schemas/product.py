from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .category import CategoryName

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    rating: int
    image_url: str

class ProductCreate(ProductBase):
    category_id: int

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    # Campos de tiempo
    created_at: datetime  # <-- Hora de creación
    updated_at: datetime  # <-- Hora de la última actualización
    
    category: Optional[CategoryName] 

    class Config:
        # FastAPI/Pydantic usará estos campos para formatear la respuesta
        orm_mode = True
        

class ProductFilterParams(BaseModel):
    # No necesita decoradores de Field con 'Query' o 'Body' aquí
    categories: Optional[List[str]] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None