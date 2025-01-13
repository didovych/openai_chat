def get_order_status(order_number):
    if order_number % 2 == 0:
        return "AWAITING_PAYMENT"
    else:
        return "READY"

def change_delivery_address(order_number, new_address):
    return True