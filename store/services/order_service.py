from store.store_memory import STORE

class OrderService:

    @staticmethod
    def _validate_coupon(code):
        # check if coupon code is in current coupon
        
        if STORE["current_coupon"]["code"] != code:
            raise Exception("Invalid coupon code")
        
        # check if coupon is already used
        if STORE["current_coupon"]["used"]:
            raise Exception("Coupon already used")
        
        # check if coupon is expired
        if STORE["current_coupon"]["expired"]:
            raise Exception("Coupon expired")

        return STORE["current_coupon"]

    @staticmethod
    def create_order(user_id, applied_coupon=None):
        cart = STORE["carts"].get(user_id, [])

        if not cart:
            raise Exception("Cart is empty")

         # calculate total amount
        total_amount = sum(item["price"] * item["quantity"] for item in cart)
        total_items = sum(item["quantity"] for item in cart)

        discount_amount = 0

        # apply coupon if provided
        if applied_coupon:
            current_coupon = OrderService._validate_coupon(applied_coupon)

            # apply 10% discount
            discount_amount = total_amount * 0.10
            current_coupon["used"] = True

            # move used coupon to history
            STORE["coupons_history"].append(current_coupon)
            STORE["current_coupon"] = None

        final_amount = total_amount - discount_amount

        # create order
        order = {
            "order_id": len(STORE["orders"]) + 1,
            "user_id": user_id,
            "items": cart,
            "total_amount": total_amount,
            "discount_applied": discount_amount,
            "final_amount": final_amount,
        }

        # save order
        STORE["orders"].append(order)

        # global analytics update
        STORE["total_orders"] += 1
        STORE["total_items"] += total_items
        STORE["total_purchase_amount"] += total_amount
        STORE["total_discount_amount"] += discount_amount

        # expire previous coupon when nth order is reached
        nth = STORE["nth"]
        if STORE["total_orders"] % nth == 0:
            prev = STORE["current_coupon"]
            if prev:
                prev["expired"] = True
                STORE["coupons_history"].append(prev)
                STORE["current_coupon"] = None

        # clear cart
        STORE["carts"][user_id] = []

        return order