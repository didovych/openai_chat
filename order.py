import random

class Order:
    def get_order_status(self, order_number: str) -> str:
        """
        Get order status by order number. The order number is a 6-character string.

        Args:
            order_number (str): The customer's order number. For example, "AD1234".
        Returns:
            str: The order status.
        """
        if len(order_number) != 6:
            return "Invalid order number."

        # randomly return order status
        rand = random.randint(1, 10)
        if rand <= 3:
            return "Order has been placed."
        elif rand <= 6:
            return "Order is being processed."
        elif rand <= 8:
            return "Order is out for delivery."
        else:
            return "Order has been delivered."

    def change_delivery_address(self, order_number: int, new_address: str) -> bool:
        """
        Change the delivery address of an order.

        Args:
            order_number (int): The customer's order number.
            new_address (str): The new delivery address.
        Returns:
            bool: True if the address was successfully changed.
        """
        return True