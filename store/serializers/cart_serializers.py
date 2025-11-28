from rest_framework import serializers

class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    item_id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.FloatField()
    quantity = serializers.IntegerField(min_value=1)

class GetCartSerializer(serializers.Serializer):
    user_id = serializers.CharField()