from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db 
from app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from app.services.cart_service import CartService 

# Inicialización del Router
cart_router = APIRouter(prefix="/users/{user_id}/cart", tags=["Cart"])

# Dependency Injector
def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    """Retorna una instancia del servicio de carrito con la sesión de BD inyectada."""
    return CartService(db)

# Helper para verificar si el usuario existe (deberías tener un servicio de User)
# Por simplicidad, asumimos que el user_id es válido o se maneja en el servicio.
# Un endpoint de auth real usaría el token del usuario logueado en lugar de {user_id} en la URL.

# ----------------------------------------------------
# 1. READ (Obtener Carrito)
# ----------------------------------------------------
@cart_router.get("/", response_model=CartResponse)
def get_user_cart(
    user_id: int, 
    service: CartService = Depends(get_cart_service)
):
    """Obtiene el carrito de un usuario. Lo crea si no existe."""
    cart = service.get_cart_for_user(user_id)
    
    if cart is None:
        # En una aplicación real, verificarías si el User existe aquí
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado."
        )
    return cart

# ----------------------------------------------------
# 2. ADD/UPDATE Item (Añadir al carrito)
# ----------------------------------------------------
@cart_router.post("/", response_model=CartResponse, status_code=status.HTTP_200_OK)
def add_item_to_cart(
    user_id: int, 
    item_data: CartItemCreate,
    service: CartService = Depends(get_cart_service)
):
    """
    Añade un producto al carrito. Si ya existe, incrementa la cantidad.
    """
    try:
        updated_cart = service.add_or_update_item(user_id, item_data)
    except ValueError as e:
        if "Product not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Producto no encontrado."
            )
        raise e
        
    return updated_cart

# ----------------------------------------------------
# 3. UPDATE Quantity (Establecer cantidad específica)
# ----------------------------------------------------
@cart_router.put("/", response_model=CartResponse)
def update_item_in_cart(
    user_id: int, 
    item_data: CartItemUpdate,
    service: CartService = Depends(get_cart_service)
):
    """
    Establece la cantidad de un ítem. Si quantity <= 0, elimina el ítem.
    """
    updated_cart = service.update_item_quantity_explicit(user_id, item_data)
    
    if updated_cart is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item no encontrado en el carrito o usuario inválido."
        )
    return updated_cart

# ----------------------------------------------------
# 4. DELETE Item
# ----------------------------------------------------
@cart_router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    user_id: int,
    product_id: int,
    service: CartService = Depends(get_cart_service)
):
    """Elimina un producto específico del carrito."""
    success = service.remove_item_from_cart(user_id, product_id)
    if not success:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item no encontrado en el carrito o usuario inválido."
        )
    return

# ----------------------------------------------------
# 5. DELETE All Items (Vaciar Carrito)
# ----------------------------------------------------
@cart_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_user_cart(
    user_id: int,
    service: CartService = Depends(get_cart_service)
):
    """Vacía completamente el carrito de un usuario."""
    success = service.empty_cart(user_id)
    if not success:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Carrito no encontrado."
        )
    return
