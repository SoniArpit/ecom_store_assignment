STORE = {
    "carts": {},
    "orders": {},
    "current_coupon": None, # example: { "code": "SAVE10", "is_used": False}
    "coupons_history": [], # History of previously generated coupons (used or expired)
    "total_orders": 0,   
    "total_items": 0,    
    "total_purchase_amount": 0.0,
    "total_discount_amount": 0.0,
    # Nth order threshold for coupon eligibility
    "nth": 5,   
}