import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ORDERS_FILE = BASE_DIR / "fake_orders.json"

with open(ORDERS_FILE, "r") as file:
    ORDERS = json.load(file)


def get_order(order_id: str) -> dict:
    """
    Fetch complete order information.
    """

    for order in ORDERS:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}


def get_shipping(order_id: str) -> dict:
    """
    Fetch shipping status for an order.
    """

    for order in ORDERS:
        if order["order_id"] == order_id:
            return {
                "order_id": order_id,
                "shipping_status": order["shipping_status"]
            }

    return {"error": "Shipping info not found"}


def check_refund_policy(category: str) -> dict:
    """
    Check refund policy for a category.
    """

    policies = {
        "electronics": "7-day refund allowed for undamaged products.",
        "fashion": "10-day exchange available.",
        "furniture": "Replacement only for damaged items.",
        "home-appliances": "5-day replacement policy.",
        "fitness": "7-day refund available.",
        "office": "No refund after delivery.",
        "home-decor": "Return accepted within 3 days."
    }

    return {
        "category": category,
        "policy": policies.get(category, "No refund policy found.")
    }


def escalate_to_human(reason: str) -> dict:
    """
    Escalate customer issue to human support.
    """

    return {
        "status": "ESCALATED",
        "message": "A human support agent will contact the customer shortly.",
        "reason": reason
    }