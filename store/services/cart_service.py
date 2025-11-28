from store.store_memory import STORE

class CartService:

    @staticmethod
    def add_item(data):
        user_id = data["user_id"]

        if user_id not in STORE["carts"]:
            STORE["carts"][user_id] = []

        # item id should be unique
        if data["item_id"] in [item["item_id"] for item in STORE["carts"][user_id]]:
            return {
                "message": "Item already exists in cart",
                "cart": STORE["carts"][user_id]
            }

        STORE["carts"][user_id].append({
            "item_id": data["item_id"],
            "name": data["name"],
            "price": data["price"],
            "quantity": data["quantity"]
        })

        return {
            "message": "Item added to cart",
            "cart": STORE["carts"][user_id]
        }
    

    @staticmethod
    def get_cart(user_id):
        cart = STORE["carts"].get(user_id, [])
        return {
            "user_id": user_id,
            "cart": cart
        }