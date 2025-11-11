# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session, select
# from ..core.database import get_session
# from ..models.cart_item import CartItem, CartItemCreate, CartItemRead
# from ..models.product import Product

# cart_item_router = APIRouter(prefix="/cart", tags=["Cart"])

# @cart_item_router.get("/", response_model=list[CartItemRead])
# def get_cart(session: Session = Depends(get_session)):
#     return session.exec(select(CartItem)).all()

# @cart_item_router.post("/", response_model=CartItemRead)
# def add_to_cart(item: CartItemCreate, session: Session = Depends(get_session)):
#     product = session.get(Product, item.product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Producto no encontrado")
#     if product.stock < item.quantity:
#         raise HTTPException(status_code=400, detail="Stock insuficiente")
#     product.stock -= item.quantity
#     db_item = CartItem.from_orm(item)
#     session.add_all([db_item, product])
#     session.commit()
#     session.refresh(db_item)
#     return db_item

# @cart_item_router.delete("/{item_id}", response_model=dict)
# def remove_from_cart(item_id: int, session: Session = Depends(get_session)):
#     item = session.get(CartItem, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item no encontrado")
#     session.delete(item)
#     session.commit()
#     return {"message": "Item eliminado del carrito"}


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cart_item import CartItemCreate, CartItemResponse
from app.repositories.cart_item_repository import add_item_to_cart

cart_item_router = APIRouter(prefix="/cart-items", tags=["Cart Items"])

@cart_item_router.post("/{cart_id}", response_model=CartItemResponse)
def add_item(cart_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    return add_item_to_cart(db, cart_id, item)
