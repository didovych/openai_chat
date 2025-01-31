from typing import List

class Store:
    def __init__(self):
        self.orders = [
            {"order_number": "FD4587", "price": 100.0, "item": "T-shirt", "status": "Order has been delivered."},
            {"order_number": "DW4578", "price": 200.0, "item": "Shoes", "status": "Order is out for delivery."},
            {"order_number": "XX3322", "price": 150.0, "item": "Hat", "status": "Order is being processed."},
            {"order_number": "BV0145", "price": 300.0, "item": "Jacket", "status": "Order has been placed."},
            {"order_number": "MN4561", "price": 250.0, "item": "Jeans", "Status": "Order has been delivered."},
        ]

    def get_order_status(self, order_number: str) -> str:
        """
        Get the order status by order numbers. The order number is a 6-character string.

        Args:
            order_number (str): The customer's order number.
        Returns:
            str: The order status.
        """
        # find order by order number
        order = next((order for order in self.orders if order["order_number"] == order_number), None)

        # check if order exists
        if not order:
            return "Order not found."

        return order["status"]

    def get_order_numbers_under_the_price(self, price: int) -> List[str]:
        """
        Returns a list of order numbers that are under the specified price.

        Args:
            price (int): The price limit to filter orders.

        Returns:
            List[str]: A list of order numbers under the specified price.
        """

        # Filter orders based on price
        filtered_orders = [order for order in self.orders if order["price"] <= price]

        order_numbers = [order["order_number"] for order in filtered_orders]

        return order_numbers

    def cancel_order(self, order_number: str):
        """
        Cancels the order.

        Args:
            order_number (str): The customer's order number. For example, "AD1234".

        Returns:
            bool: True if the order was successfully canceled, False otherwise.
        """
        # find order by order number
        order = next((order for order in self.orders if order["order_number"] == order_number), None)

        # check if order exists
        if not order:
            return False

        # cancel order
        order["status"] = "Order has been canceled."

        return True

    def get_all_orders(self) -> List[dict]:
        """
        Returns all orders.

        Returns:
            List[dict]: A list of all orders.
        """
        return self.orders