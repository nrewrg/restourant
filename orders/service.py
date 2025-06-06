from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select

from fastapi import HTTPException

from products import service as products_service

from users import User

from carts import service as carts_service

from http_exceptions import AccessDenied

from .models import Order, Status


async def create(user_id: int, db_session: AsyncSession):
    """
    Create a new order from the user's cart.

    Args:
        user_id (int): The ID of the user placing the order.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 400 if the user's cart is empty.

    Returns:
        dict: A dictionary containing a success message and the created order instance.
    """
    cart = await carts_service.get(user_id, db_session)
    if cart.products == {}:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(**cart.model_dump())
    cart.products = {}
    cart.total_price = 0

    db_session.add(cart)
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    return {"message": "Order created", "order": order}


async def get(id: int, current_user: User, db_session: AsyncSession):
    """
    Retrieve an order by its ID, enforcing access control.

    Args:
        id (int): The ID of the order to retrieve.
        current_user (User): The user requesting the order.
        db_session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException:
            - 404 if the order does not exist.
        AccessDenied:
            - If the current user is neither the owner of the order nor an admin.

    Returns:
        Order: The order instance with the specified ID.
    """
    res = await db_session.exec(select(Order).where(Order.id == id))
    order = res.first()
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order with id {id} not found")

    if current_user.id != order.user_id:
        if current_user.role != "admin":
            raise AccessDenied()
    return order


async def get_with_user_id(user_id: int, db_session: AsyncSession):
    """
    Retrieve all orders for a specific user.

    Args:
        user_id (int): The ID of the user whose orders to retrieve.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Order]: A list of orders belonging to the specified user.
    """
    res = await db_session.exec(select(Order).where(Order.user_id == user_id))
    orders = res.all()

    return orders


async def get_all(db_session: AsyncSession):
    """
    Retrieve all orders in the system.

    Args:
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        List[Order]: A list of all order instances.
    """
    res = await db_session.exec(select(Order))
    orders = res.all()

    return orders


async def update_status(
    id: int, status: Status, current_user: User, db_session: AsyncSession
):
    """
    Update the status of an order.

    Args:
        id (int): The ID of the order to update.
        status (Status): The new status to set for the order.
        current_user (User): The user requesting the status update.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        dict: A dictionary containing a success message and the updated order instance.
    """
    order = await get(id, current_user, db_session)

    order.status = status

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    return {"message": "Order status updated", "order": order}
