from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from store.serializers.checkout_serializers import CheckoutSerializer
from store.services.order_service import OrderService
from utils.response_utils import success, error


@extend_schema(tags=["Checkout"])
class CheckoutView(APIView):

    @extend_schema(
        request=CheckoutSerializer,
        responses={200: None},
        summary="Checkout cart",
        description="Creates an order, applies coupon if provided, updates totals, and clears cart."
    )
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            order = OrderService.create_order(
                user_id=data["user_id"],
                applied_coupon=data.get("coupon")
            )
            return success(order)
        except Exception as e:
            return error(str(e))