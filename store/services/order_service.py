from store.store_memory import STORE

class OrderService:

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
            current_coupon = STORE["current_coupon"]

            if not current_coupon:
                raise Exception("No coupon available")

            if current_coupon["expired"]:
                raise Exception("Coupon is expired")

            if current_coupon["used"]:
                raise Exception("Coupon is already used")

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

        # 🔥 UPDATE GLOBAL ANALYTICS (you were missing this)
        STORE["total_orders"] += 1
        STORE["total_items"] += total_items
        STORE["total_purchase_amount"] += total_amount
        STORE["total_discount_amount"] += discount_amount

        # clear cart
        STORE["carts"][user_id] = []

        return order