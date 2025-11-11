from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False) 
    description = Column(String(500)) 
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String(500))

    category = relationship("Category", back_populates="products")
    
