from rest_framework import serializers

class CouponSerializer(serializers.Serializer):
    code = serializers.CharField()
    is_used = serializers.BooleanField()

class AnalyticsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_items_purchased = serializers.IntegerField()
    total_purchase_amount = serializers.FloatField()
    total_discount_amount = serializers.FloatField()
    coupons_history = CouponSerializer(many=True)
    current_coupon = CouponSerializer(allow_null=True)