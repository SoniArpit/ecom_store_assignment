from rest_framework.test import APITestCase
from store.store_memory import STORE


class CartTests(APITestCase):
    def setUp(self):
        # reset in-memory store before each test
        STORE["carts"].clear()
        STORE["orders"].clear()
        STORE["current_coupon"] = None
        STORE["coupons_history"].clear()
        STORE["total_orders"] = 0
        STORE["total_items"] = 0
        STORE["total_purchase_amount"] = 0.0
        STORE["total_discount_amount"] = 0.0

        self.url = "/api/store/cart/"

    def test_add_item_to_cart(self):
        # basic test to ensure add-to-cart works
        payload = {
            "user_id": "u1",
            "item_id": "i1",
            "name": "Keyboard",
            "price": 500,
            "quantity": 1
        }

        res = self.client.post(self.url, payload, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["success"])

        # cart should now have 1 item
        self.assertEqual(len(STORE["carts"]["u1"]), 1)

    def test_get_cart_items(self):
        # manually populate cart before GET
        STORE["carts"]["u1"] = [
            {"item_id": "i1", "name": "Mouse", "price": 300, "quantity": 2}
        ]

        res = self.client.get(self.url, {"user_id": "u1"})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["success"])

        cart = res.data["data"]["cart"]
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]["name"], "Mouse")

    def test_get_cart_when_empty(self):
        # empty cart should just return empty list
        res = self.client.get(self.url, {"user_id": "no_user"})
        self.assertEqual(res.status_code, 200)

        cart = res.data["data"]["cart"]
        self.assertEqual(cart, [])  # empty cart is fine

    def test_add_duplicate_item(self):
        # add item first
        payload = {
            "user_id": "u1",
            "item_id": "i1",
            "name": "Keyboard",
            "price": 500,
            "quantity": 1
        }
        self.client.post(self.url, payload, format="json")

        # try adding same item again
        res = self.client.post(self.url, payload, format="json")
        self.assertEqual(res.status_code, 200)
        
        # check message says it already exists
        self.assertIn("already exists", res.data["data"]["message"])
        
        # count should still be 1
        self.assertEqual(len(STORE["carts"]["u1"]), 1)
