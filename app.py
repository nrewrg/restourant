from fastapi import FastAPI

from users import router as users_router
from auth import router as auth_router
from categories import router as categories_router
from products import router as products_router
from carts import router as carts_router
from orders import router as orders_router
from reservations import router as reservations_router


app = FastAPI(title="Restaraunt API", version="v1")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(carts_router)
app.include_router(orders_router)
app.include_router(reservations_router)
