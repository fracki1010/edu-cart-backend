from sqlalchemy.orm import Session
from typing import Optional

from app.models.cart import Cart
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository # Necesario para verificar productos

class CartService:
    """
    Clase que contiene la lógica de negocio para la gestión del Carrito de Compras.
    """
    def __init__(self, db: Session):
        self.repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    def get_cart_for_user(self, user_id: int) -> Optional[Cart]:
        """Obtiene el carrito existente o None si el usuario no existe (debe ser verificado en el Router)."""
        return self.repository.get_cart_by_user_id(user_id)

    def add_or_update_item(self, user_id: int, item_data: CartItemCreate) -> Cart:
        """Agrega un producto al carrito o actualiza su cantidad si ya existe."""
        
        # 1. Verificar si el producto existe
        product = self.product_repository.get_by_id(item_data.product_id)
        if product is None:
            # En una aplicación real, se lanzaría una excepción específica para el router
            raise ValueError("Product not found") 

        # 2. Obtener o crear el carrito
        cart = self.repository.get_or_create_cart(user_id)
        
        # 3. Buscar el ítem existente
        existing_item = self.repository.get_item(cart.id, item_data.product_id)
        
        if existing_item:
            # Si existe, actualiza la cantidad sumando (lógica de añadir)
            new_quantity = existing_item.quantity + item_data.quantity
            self.repository.update_item_quantity(existing_item, new_quantity)
        else:
            # Si no existe, crea un nuevo ítem
            self.repository.add_item(cart.id, item_data.product_id, item_data.quantity)
            
        # Vuelve a cargar el carrito completo para la respuesta (opciones de joinedload ya están en el repo)
        return self.repository.get_cart_by_user_id(user_id)

    def update_item_quantity_explicit(self, user_id: int, item_data: CartItemUpdate) -> Optional[Cart]:
        """Establece explícitamente la cantidad de un producto en el carrito."""
        cart = self.repository.get_cart_by_user_id(user_id)
        if cart is None:
            return None # El Router manejará el 404
        
        existing_item = self.repository.get_item(cart.id, item_data.product_id)
        
        if existing_item:
            if item_data.quantity <= 0:
                 self.repository.remove_item(existing_item)
            else:
                self.repository.update_item_quantity(existing_item, item_data.quantity)
        else:
            # Item no encontrado en el carrito
            return None 

        return self.repository.get_cart_by_user_id(user_id)


    def remove_item_from_cart(self, user_id: int, product_id: int) -> bool:
        """Elimina un producto del carrito."""
        cart = self.repository.get_cart_by_user_id(user_id)
        if cart is None:
            return False

        existing_item = self.repository.get_item(cart.id, product_id)
        
        if existing_item:
            self.repository.remove_item(existing_item)
            return True
        return False
        
    def empty_cart(self, user_id: int) -> bool:
        """Vacía completamente el carrito de un usuario."""
        cart = self.repository.get_cart_by_user_id(user_id)
        if cart is None:
            return False
            
        self.repository.clear_cart(cart)
        return True
