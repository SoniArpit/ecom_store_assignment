from rest_framework.test import APITestCase
from store.store_memory import STORE


class CouponTests(APITestCase):
    def setUp(self):
        # reset everything before each test
        STORE["carts"].clear()
        STORE["orders"].clear()
        STORE["current_coupon"] = None
        STORE["coupons_history"].clear()
        STORE["total_orders"] = 0
        STORE["total_items"] = 0
        STORE["total_purchase_amount"] = 0.0
        STORE["total_discount_amount"] = 0.0

        self.generate_url = "/api/store/admin/generate-coupon/"
        self.checkout_url = "/api/store/checkout/"
        self.cart_url = "/api/store/cart/"

    def _add_item(self, user="u1"):
        """Small helper to avoid repeating payloads."""
        payload = {
            "user_id": user,
            "item_id": "i1",
            "name": "Test Item",
            "price": 100,
            "quantity": 1,
        }
        self.client.post(self.cart_url, payload, format="json")

    def _checkout(self, user="u1", coupon=None):
        """Helper to perform checkout."""
        body = {"user_id": user}
        if coupon:
            body["coupon"] = coupon
        return self.client.post(self.checkout_url, body, format="json")

    def test_coupon_generation_not_allowed_before_nth(self):
        # no orders yet → shouldn't allow coupon
        res = self.client.post(self.generate_url, {}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("Not eligible", res.data["error"])

    def test_coupon_generated_on_nth_order(self):
        # place 5 orders (assuming nth = 5)
        for _ in range(5):
            self._add_item()
            self._checkout()

        # now coupon generation must be allowed
        res = self.client.post(self.generate_url, {}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["success"])

        self.assertIsNotNone(STORE["current_coupon"])
        self.assertFalse(STORE["current_coupon"]["expired"])

    def test_coupon_expires_on_next_nth(self):
        # reach order #5
        for _ in range(5):
            self._add_item()
            self._checkout()

        # generate coupon C1
        self.client.post(self.generate_url, {}, format="json")
        c1 = STORE["current_coupon"]["code"]

        # now complete next 5 orders → total orders = 10 (next nth)
        for _ in range(5):
            self._add_item()
            self._checkout()

        # old coupon should be expired automatically
        self.assertIsNone(STORE["current_coupon"])  # no active coupon now
        self.assertTrue(STORE["coupons_history"][-1]["expired"])

    def test_old_coupon_cannot_be_used(self):
        # reach order #5
        for _ in range(5):
            self._add_item()
            self._checkout()

        # generate coupon C1
        self.client.post(self.generate_url, {}, format="json")
        c1 = STORE["current_coupon"]["code"]

        # reach next nth (order #10) so coupon is expired
        for _ in range(5):
            self._add_item()
            self._checkout()

        # try using old C1
        self._add_item()
        res = self._checkout(coupon=c1)

        self.assertEqual(res.status_code, 400)
        self.assertIn("invalid", res.data["error"].lower())

    def test_used_coupon_cannot_be_used_again(self):
        # reach order #5 and generate coupon
        for _ in range(5):
            self._add_item()
            self._checkout()

        self.client.post(self.generate_url, {}, format="json")
        c1 = STORE["current_coupon"]["code"]

        # first use → should work
        self._add_item()
        first_res = self._checkout(coupon=c1)
        self.assertEqual(first_res.status_code, 200)

        # second use → must fail
        self._add_item()
        second_res = self._checkout(coupon=c1)
        self.assertEqual(second_res.status_code, 400)
        self.assertIn("invalid", second_res.data["error"].lower())
