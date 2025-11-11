from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilterParams
from ..repositories.product_repository import ProductRepository

class ProductService:
    """
    Clase que contiene la lógica de negocio para los Productos.
    Coordina la interacción entre la capa de presentación (Router) y la capa de datos (Repository).
    """
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.db = db

    def get_filtered_products(self, filters: ProductFilterParams) -> List[Product]:
        query = self.db.query(Product).options(joinedload(Product.category))

        # --- 1. Filtrar por Categorías (por nombre) ---
        if filters and filters.categories:
            query = query.join(Product.category).filter(Category.name.in_(filters.categories))

        # --- 2. Filtrar por Rango de Precios ---
        if filters and filters.price_min is not None:
            query = query.filter(Product.price >= filters.price_min)

        if filters and filters.price_max is not None:
            query = query.filter(Product.price <= filters.price_max)

        # --- 3. Ejecutar y retornar resultados ---
        return query.all()


    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Recupera un producto y lanza excepción si no existe."""
        product = self.repository.get_by_id(product_id)
        if product is None:
            # En una aplicación FastAPI real, lanzarías una HTTPException aquí
            # raise HTTPException(status_code=404, detail="Product not found")
            return None # Dejamos el manejo de error 404 para el Router
        return product

    def create_product(self, product_data: ProductCreate) -> Product:
        """Crea un nuevo producto."""
        # Aquí iría la lógica de negocio, ej: validar stock inicial, verificar categoría activa, etc.
        return self.repository.create(product_data)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Actualiza un producto existente."""
        product = self.get_product_by_id(product_id)
        if product is None:
            return None
        
        return self.repository.update(product, product_data)

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto."""
        product = self.get_product_by_id(product_id)
        if product is None:
            return False # No se pudo eliminar porque no existe

        self.repository.delete(product)
        return True
