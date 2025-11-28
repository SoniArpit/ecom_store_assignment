from rest_framework import serializers

class CheckoutSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    coupon = serializers.CharField(required=False, allow_blank=True)
