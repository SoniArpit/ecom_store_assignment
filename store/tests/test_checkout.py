from rest_framework.test import APITestCase
from store.store_memory import STORE


class CheckoutTests(APITestCase):
    def setUp(self):
        # Reset memory store before every test
        STORE["carts"].clear()
        STORE["orders"].clear()
        STORE["current_coupon"] = None
        STORE["coupons_history"].clear()
        STORE["total_orders"] = 0
        STORE["total_items"] = 0
        STORE["total_purchase_amount"] = 0.0
        STORE["total_discount_amount"] = 0.0

        self.cart_url = "/api/store/cart/"
        self.checkout_url = "/api/store/checkout/"

    def _add_item(self, user="u1"):
        """Helper to add a basic item to cart. Just saves repeating payloads."""
        payload = {
            "user_id": user,
            "item_id": "i1",
            "name": "Test Item",
            "price": 100,
            "quantity": 2,
        }
        self.client.post(self.cart_url, payload, format="json")

    def test_checkout_without_coupon(self):
        # simple case: no coupon involved
        self._add_item()
        res = self.client.post(self.checkout_url, {"user_id": "u1"}, format="json")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["success"])

        # order should store correct totals
        order = res.data["data"]
        self.assertEqual(order["total_amount"], 200)  # 100 * qty 2
        self.assertEqual(order["discount_applied"], 0)
        self.assertEqual(order["final_amount"], 200)

        # order count should increment
        self.assertEqual(STORE["total_orders"], 1)

    def test_checkout_with_active_coupon(self):
        # add item first
        self._add_item()

        # manually set an active coupon
        STORE["current_coupon"] = {
            "code": "ABC123",
            "used": False,
            "expired": False,
        }

        payload = {"user_id": "u1", "coupon": "ABC123"}
        res = self.client.post(self.checkout_url, payload, format="json")

        self.assertEqual(res.status_code, 200)

        data = res.data["data"]

        # final amount should be 10% off
        self.assertEqual(data["discount_applied"], 20)  # 10% of 200
        self.assertEqual(data["final_amount"], 180)

        # coupon should now be used & moved to history
        self.assertIsNone(STORE["current_coupon"])
        self.assertEqual(len(STORE["coupons_history"]), 1)
        self.assertTrue(STORE["coupons_history"][0]["used"])

    def test_checkout_with_invalid_coupon(self):
        self._add_item()

        # active coupon has different code
        STORE["current_coupon"] = {
            "code": "XYZ999",
            "used": False,
            "expired": False,
        }

        payload = {"user_id": "u1", "coupon": "WRONGCODE"}
        res = self.client.post(self.checkout_url, payload, format="json")

        # should reject immediately
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.data["success"])

    def test_checkout_with_expired_coupon(self):
        self._add_item()

        STORE["current_coupon"] = {
            "code": "HELLO10",
            "used": False,
            "expired": True,
        }

        payload = {"user_id": "u1", "coupon": "HELLO10"}
        res = self.client.post(self.checkout_url, payload, format="json")

        self.assertEqual(res.status_code, 400)
        self.assertIn("expired", res.data["error"].lower())

    def test_checkout_with_used_coupon(self):
        self._add_item()

        STORE["current_coupon"] = {
            "code": "USED10",
            "used": True,
            "expired": False,
        }

        payload = {"user_id": "u1", "coupon": "USED10"}
        res = self.client.post(self.checkout_url, payload, format="json")

        self.assertEqual(res.status_code, 400)
        self.assertIn("used", res.data["error"].lower())

    def test_checkout_clears_cart(self):
        self._add_item()

        self.client.post(self.checkout_url, {"user_id": "u1"}, format="json")

        # after checkout cart should be empty
        self.assertEqual(STORE["carts"]["u1"], [])

    def test_checkout_empty_cart(self):
        # try checkout without adding items
        res = self.client.post(self.checkout_url, {"user_id": "u_empty"}, format="json")
        
        self.assertEqual(res.status_code, 400)
        self.assertIn("empty", res.data["error"].lower())