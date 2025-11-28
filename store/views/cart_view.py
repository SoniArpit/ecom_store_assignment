from store.serializers.cart_serializers import GetCartSerializer
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from store.serializers.cart_serializers import AddToCartSerializer
from store.services.cart_service import CartService
from utils.response_utils import success

@extend_schema(tags=["Cart"])
class CartView(APIView):
    """
    POST: Add item to cart
    GET: Get cart items
    """
    @extend_schema(
        request=AddToCartSerializer,
        responses={200: None},
        summary="Add item to cart",
        description="Adds an item to the user's in-memory cart."
    )
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = CartService.add_item(serializer.validated_data)
        return success(data)


    @extend_schema(
        parameters=[GetCartSerializer],
        responses={200: None},
        summary="Get user cart",
        description="Returns all items currently in the user's in-memory cart."
    )
    def get(self, request):
        serializer = GetCartSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = CartService.get_cart(serializer.validated_data["user_id"])
        return success(data)