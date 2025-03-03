from typing import Annotated

from pydantic import BaseModel, Field, EmailStr

#User classes
class UserBase(BaseModel):
    username: Annotated[
        str,
        Field(..., title="Username", min_length=3, max_length=20)
    ]
    age: Annotated[
        int,
        Field(..., title="User age", ge=1, lt=120)
    ]
    email: EmailStr

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

#Product classes

class ProductBase(BaseModel):
    name: Annotated[
        str,
        Field(..., title="Product name", min_length=2, max_length=30)
    ]
    price: Annotated[
        float,
        Field(..., title="Product price", ge=0)
    ]

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass

#Cart classes
class CartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: Annotated[int, Field(..., title="Product quantity", ge=1)]

class Cart(CartBase):
    id: int
    user: User
    product: Product
    class Config:
        orm_mode = True

class CartCreate(CartBase):
    pass
