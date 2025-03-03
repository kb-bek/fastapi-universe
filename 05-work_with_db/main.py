from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from models import Base, User, Product, Cart
from database import engine, session_local
from schemas import UserCreate, ProductCreate, CartCreate, User as UserResponse, Product as ProductResponse, Cart as CartResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


#Enpoints for User
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    new_user = User(username=user.username, age=user.age, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    users = db.query(User).all()
    return users

@app.get("/users/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.delete("/users/{id}/delete")
def delete_user(id:int, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User was deleted"}


#Enpoints for Product

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> ProductResponse:
    new_product = Product(name=product.name, price=product.price)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)) -> List[ProductResponse]:
    products = db.query(Product).all()

    return products

@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.delete("/products/{id}/delete")
def delete_product(id: int, db: Session = Depends(get_db)) -> dict:
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

    return {"message": "Product was deleted"}


#Endpoints for Cart

@app.post("/addToCart", response_model=CartResponse)
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == cart.user_id).first()
    product = db.query(Product).filter(Product.id == cart.product_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_cart_item = db.query(Cart).filter(Cart.user_id == cart.user_id, Cart.product_id == cart.product_id).first()
    if existing_cart_item:

        existing_cart_item.quantity += cart.quantity
        db.commit()
        db.refresh(existing_cart_item)
        return existing_cart_item

    new_cart = Cart(user_id=cart.user_id, product_id=cart.product_id, quantity=cart.quantity)

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return new_cart


@app.get("/carts", response_model=List[CartResponse])
def get_carts(db: Session = Depends(get_db)):
    carts = db.query(Cart).all()

    return carts


@app.get("/carts/{id}", response_model=CartResponse)
def get_cart_by_id(id:int, db: Session = Depends(get_db)) -> CartResponse:
    cart = db.query(Cart).filter(Cart.id == id).first()

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


@app.delete("/carts/{id}/delete")
def delete_cart(id:int, db: Session = Depends(get_db)) -> dict:
    cart = db.query(Cart).filter(Cart.id == id).first()

    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.delete(cart)
    db.commit()

    return {"message": "Cart was deleted"}






