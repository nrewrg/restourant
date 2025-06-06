from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select

from fastapi import HTTPException

from products import service as products_service

from .models import Cart


async def create(user_id: int, db_session: AsyncSession):
    """
    Create a new cart for a user.

    Args:
        user_id (int): The ID of the user for whom to create the cart.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        Cart: The newly created cart instance.
    """
    cart = Cart(user_id=user_id)

    db_session.add(cart)
    await db_session.commit()
    await db_session.refresh(cart)

    return cart


async def get(user_id: int, db_session: AsyncSession):
    """
    Retrieve the cart for a given user. Creates a new cart if none exists.

    Args:
        user_id (int): The ID of the user whose cart to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        Cart: The user's cart instance.
    """
    res = await db_session.exec(select(Cart).where(Cart.user_id == user_id))
    cart = res.first()

    if not cart:
        cart = await create(user_id, db_session)
    return cart


async def add_product(user_id: int, product_id: int, db_session: AsyncSession):
    """
    Add a product to the user's cart. Increments quantity if product already in cart.

    Args:
        user_id (int): The ID of the user whose cart to update.
        product_id (int): The ID of the product to add.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the quantity of the product exceeds 10.

    Returns:
        dict: A dictionary containing a success message and the updated cart instance.
    """
    cart = await get(user_id, db_session)

    product = await products_service.get(product_id, db_session)

    try:
        if cart.products[str(product_id)]["quantity"] > 9:
            raise HTTPException(
                status_code=400, detail="Max quantity for one product is 10"
            )
        cart.products = cart.products | {
            str(product_id): {
                "quantity": cart.products[str(product_id)]["quantity"] + 1,
                "price": cart.products[str(product_id)]["price"] + product.price,
            }
        }
    except KeyError:
        cart.products = cart.products | {
            str(product_id): {"quantity": 1, "price": product.price}
        }

    cart.total_price = 0
    for k, v in cart.products.items():
        cart.total_price += v["price"]

    db_session.add(cart)
    await db_session.commit()
    await db_session.refresh(cart)

    return {"message": "Product added", "cart": cart}


async def set_quantity_for_product(
    user_id: int, product_id: int, quantity: int, db_session: AsyncSession
):
    """
    Set the quantity for a specific product in the user's cart.
    Removes the product if quantity is less than 1.

    Args:
        user_id (int): The ID of the user whose cart to update.
        product_id (int): The ID of the product to update.
        quantity (int): The desired quantity for the product.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if quantity exceeds 10.

    Returns:
        dict: A dictionary containing a success message and the updated cart instance.
    """
    cart = await get(user_id, db_session)

    product = await products_service.get(product_id, db_session)

    if quantity > 10:
        raise HTTPException(
            status_code=400, detail="Max quantity for one product is 10"
        )
    elif quantity < 1:
        cart.products = {k: v for k, v in cart.products.items() if k != str(product.id)}
    else:
        cart.products = cart.products | {
            str(product.id): {
                "quantity": quantity,
                "price": product.price * quantity,
            }
        }

    cart.total_price = 0
    for k, v in cart.products.items():
        cart.total_price += v["price"]

    db_session.add(cart)
    await db_session.commit()
    await db_session.refresh(cart)

    return {"message": "Quantity set", "cart": cart}


async def remove_product(user_id: int, product_id: int, db_session: AsyncSession):
    """
    Remove one unit of a product from the user's cart.
    Removes the product entirely if quantity reaches zero.

    Args:
        user_id (int): The ID of the user whose cart to update.
        product_id (int): The ID of the product to remove.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the product is not found in the cart.

    Returns:
        dict: A dictionary containing a success message and the updated cart instance.
    """
    cart = await get(user_id, db_session)

    try:
        if cart.products[str(product_id)]["quantity"] == 1:
            cart.products = {
                k: v for k, v in cart.products.items() if k != str(product_id)
            }
        else:
            product = await products_service.get(product_id, db_session)
            cart.products = cart.products | {
                str(product_id): {
                    "quantity": cart.products[str(product.id)]["quantity"] - 1,
                    "price": cart.products[str(product.id)]["price"] - product.price,
                }
            }
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"There is no product with id {product_id} in user cart",
        )

    cart.total_price = 0
    for k, v in cart.products.items():
        cart.total_price += v["price"]

    db_session.add(cart)
    await db_session.commit()
    await db_session.refresh(cart)

    return {"message": "Product removed", "cart": cart}
