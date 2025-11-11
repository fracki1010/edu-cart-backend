from pydantic import BaseModel
from typing import Optional

# --- Esquemas de Categoría ---

class CategoryName(BaseModel):
    """Esquema mínimo para solo mostrar el nombre de la categoría."""
    name: str
    
    class Config:
        # Pydantic V1: Si estás usando SQLModel, no necesitas orm_mode aquí,
        # pero lo mantengo por si acaso.
        # Pydantic V2: Esto sería 'from_attributes = True'
        orm_mode = True 

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True