from store.store_memory import STORE

class AnalyticsService:
    @staticmethod
    def get_stats():
        return {
            "total_orders": STORE["total_orders"],
            "total_items_purchased": STORE["total_items"],
            "total_purchase_amount": STORE["total_purchase_amount"],
            "total_discount_amount": STORE["total_discount_amount"],

            # history list of coupons
            "coupons_history": STORE["coupons_history"],

            # currently active coupon
            "current_coupon": STORE["current_coupon"],
        }