
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductFilterParams
from ..services.product_service import ProductCreate, ProductService
from ..core.security import get_current_user

product_router = APIRouter(prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)] )

# Dependency Injector (permite usar el servicio en los endpoints)
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Retorna una instancia del servicio de productos con la sesión de BD inyectada."""
    return ProductService(db)



# ----------------------------------------------------
# 1. READ (Listar todos) - Endpoint inicial del usuario
# ----------------------------------------------------
@product_router.get("/", response_model=List[ProductResponse])
def list_products(
    categories: Optional[List[str]] = Query(None, description="Lista de categorías"),
    price_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    price_max: Optional[float] = Query(None, description="Precio máximo"),
    service: ProductService = Depends(get_product_service)
):
    filters = ProductFilterParams(
        categories=categories,
        price_min=price_min,
        price_max=price_max
    )
    return service.get_filtered_products(filters)




# ----------------------------------------------------
# 2. READ (Por ID)
# ----------------------------------------------------
@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Obtiene un producto específico por su ID."""
    product = service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado."
        )
    return product

# ----------------------------------------------------
# 3. CREATE
# ----------------------------------------------------
@product_router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate, 
    service: ProductService = Depends(get_product_service)
):
    """Crea un nuevo producto."""
    return service.create_product(product_data)

# ----------------------------------------------------
# 4. UPDATE
# ----------------------------------------------------
@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, 
    product_data: ProductUpdate, 
    service: ProductService = Depends(get_product_service)
):
    """Actualiza completamente un producto existente."""
    product = service.update_product(product_id, product_data)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado para actualizar."
        )
    return product

# ----------------------------------------------------
# 5. DELETE
# ----------------------------------------------------
@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, 
    service: ProductService = Depends(get_product_service)
):
    """Elimina un producto por su ID."""
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado para eliminar."
        )
    return