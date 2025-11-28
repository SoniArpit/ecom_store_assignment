import uuid
from store.store_memory import STORE

class CouponService:
    @staticmethod
    def _generate_coupon_code():
        """
        Generate a random coupon code of length 8
        """
        coupon_code = str(uuid.uuid4()).upper()[:8]
        return coupon_code

    
    @staticmethod
    def _is_eligible():
        """
        Check if the store is eligible to generate a new coupon
        """
        nth = STORE['nth'] # get Nth order threshold for coupon eligibility
        return STORE["total_orders"] > 0 and STORE['total_orders'] % nth == 0
            
    
    @staticmethod
    def generate():
        """
        Generate a new coupon if eligible.
        Expire previous coupon if exists.
        """
        if not CouponService._is_eligible():
            return None, "Not eligible. Coupon can only be generated on every nth order."

        # Expire old coupon if exists
        old = STORE["current_coupon"]
        if old:
            old["expired"] = True
            STORE["coupons_history"].append(old)

        # Create new coupon
        new_coupon = {
            "code": CouponService._generate_coupon_code(),
            "used": False,
            "expired": False
        }

        STORE["current_coupon"] = new_coupon

        return new_coupon, None