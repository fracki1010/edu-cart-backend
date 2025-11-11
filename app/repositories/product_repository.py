from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    """
    Clase encargada de la persistencia de datos de la entidad Product.
    Solo contiene lógica de CRUD, sin reglas de negocio.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        """Recupera todos los productos."""
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Recupera un producto por su ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_data: ProductCreate) -> Product:
        """Crea un nuevo producto en la base de datos."""
        # Se convierte el esquema Pydantic en un modelo SQLAlchemy
        new_product = Product(**product_data.model_dump()) 
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def update(self, product: Product, product_data: ProductUpdate) -> Product:
        """Actualiza un producto existente."""
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
            
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        """Elimina un producto de la base de datos."""
        self.db.delete(product)
        self.db.commit()