from rest_framework.test import APITestCase
from store.store_memory import STORE


class GenerateCouponTests(APITestCase):
    def setUp(self):
        # clean memory store before each test
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
        self.generate_coupon_url = "/api/store/admin/generate-coupon/"

    def _add_item(self):
        payload = {
            "user_id": "u1",
            "item_id": "i1",
            "name": "Test Item",
            "price": 100,
            "quantity": 1,
        }
        self.client.post(self.cart_url, payload, format="json")

    def _checkout(self, coupon=None):
        body = {"user_id": "u1"}
        if coupon:
            body["coupon"] = coupon
        return self.client.post(self.checkout_url, body, format="json")

    def test_generate_coupon_before_nth_order_fails(self):
        # nth = 5, so with 0 orders this should fail
        res = self.client.post(self.generate_coupon_url, {}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("eligible", res.data["error"])

    def test_generate_coupon_at_exact_nth_order(self):
        # make 5 orders → now eligible
        for _ in range(5):
            self._add_item()
            self._checkout()

        res = self.client.post(self.generate_coupon_url, {}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["success"])

        # coupon must be active now
        self.assertIsNotNone(STORE["current_coupon"])
        self.assertFalse(STORE["current_coupon"]["expired"])

    def test_generate_coupon_moves_old_one_to_history(self):
        # reach 5th order and generate first coupon
        for _ in range(5):
            self._add_item()
            self._checkout()

        self.client.post(self.generate_coupon_url)
        first = STORE["current_coupon"]["code"]

        # reach next 5 orders (order #10)
        for _ in range(5):
            self._add_item()
            self._checkout()

        # generate second coupon
        res = self.client.post(self.generate_coupon_url)
        self.assertEqual(res.status_code, 200)

        # history should contain previous coupon
        self.assertGreaterEqual(len(STORE["coupons_history"]), 1)
        self.assertTrue(STORE["coupons_history"][-1]["expired"])
        self.assertIsNotNone(STORE["current_coupon"])

    def test_generate_coupon_when_previous_coupon_not_used(self):
        # reach order #5 and generate coupon C1
        for _ in range(5):
            self._add_item()
            self._checkout()

        self.client.post(self.generate_coupon_url)
        c1 = STORE["current_coupon"]["code"]

        # reach next nth (order #10)
        for _ in range(5):
            self._add_item()
            self._checkout()

        # old coupon should be auto-expired before generating new one
        res = self.client.post(self.generate_coupon_url)
        self.assertEqual(res.status_code, 200)

        self.assertIsNotNone(STORE["current_coupon"])
        # C1 should be in history, expired = True
        expired_coupon = STORE["coupons_history"][-1]
        self.assertEqual(expired_coupon["code"], c1)
        self.assertTrue(expired_coupon["expired"])

    def test_generate_coupon_overwrites_existing(self):
        # reach order #5
        for _ in range(5):
            self._add_item()
            self._checkout()

        # generate first coupon
        self.client.post(self.generate_coupon_url)
        c1 = STORE["current_coupon"]["code"]

        # generate AGAIN (still eligible as order count is 5)
        # This hits the overwrite scenario
        res = self.client.post(self.generate_coupon_url)
        self.assertEqual(res.status_code, 200)

        c2 = STORE["current_coupon"]["code"]
        self.assertNotEqual(c1, c2)

        # c1 should be in history and expired
        self.assertEqual(STORE["coupons_history"][-1]["code"], c1)
        self.assertTrue(STORE["coupons_history"][-1]["expired"])