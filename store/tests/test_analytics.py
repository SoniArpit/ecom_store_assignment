from rest_framework.test import APITestCase
from store.store_memory import STORE


class AnalyticsTests(APITestCase):
    def setUp(self):
        # Reset everything before each test
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
        self.analytics_url = "/api/store/admin/analytics/"
        self.generate_coupon_url = "/api/store/admin/generate-coupon/"

    def _add_item(self, user="u1", price=100, qty=1):
        payload = {
            "user_id": user,
            "item_id": "i1",
            "name": "Test Item",
            "price": price,
            "quantity": qty,
        }
        self.client.post(self.cart_url, payload, format="json")

    def _checkout(self, user="u1", coupon=None):
        body = {"user_id": user}
        if coupon:
            body["coupon"] = coupon
        return self.client.post(self.checkout_url, body, format="json")

    def test_analytics_without_orders(self):
        # no orders yet → everything should be zero
        res = self.client.get(self.analytics_url)
        self.assertEqual(res.status_code, 200)

        data = res.data["data"]

        self.assertEqual(data["total_orders"], 0)
        self.assertEqual(data["total_items_purchased"], 0)
        self.assertEqual(data["total_purchase_amount"], 0)
        self.assertEqual(data["total_discount_amount"], 0)
        self.assertEqual(len(data["coupons_history"]), 0)
        self.assertIsNone(data["current_coupon"])

    def test_analytics_after_normal_checkout(self):
        # add item worth 200 (100 x 2)
        self._add_item(price=100, qty=2)
        self._checkout()

        res = self.client.get(self.analytics_url)
        data = res.data["data"]

        self.assertEqual(data["total_orders"], 1)
        self.assertEqual(data["total_items_purchased"], 2)
        self.assertEqual(data["total_purchase_amount"], 200)
        self.assertEqual(data["total_discount_amount"], 0)

    def test_analytics_after_checkout_with_coupon(self):
        # reach nth order first (nth=5)
        for _ in range(5):
            self._add_item()
            self._checkout()

        # generate coupon
        res = self.client.post(self.generate_coupon_url)
        coupon = res.data["data"]["coupon"]["code"]

        # now use coupon for a purchase (100 Rs → 10% off => 10 Rs discount)
        self._add_item(price=100, qty=1)
        self._checkout(coupon=coupon)

        res = self.client.get(self.analytics_url)
        data = res.data["data"]

        # 6 total orders now
        self.assertEqual(data["total_orders"], 6)

        # items: 5 orders (each 1 item) + coupon order (1 item)
        self.assertEqual(data["total_items_purchased"], 6)

        # purchase amount = 5*100 + 100 = 600
        self.assertEqual(data["total_purchase_amount"], 600)

        # discount = 10 on sixth order
        self.assertEqual(data["total_discount_amount"], 10)

        # coupon should be in history now
        self.assertEqual(len(data["coupons_history"]), 1)
        self.assertTrue(data["coupons_history"][0]["used"])