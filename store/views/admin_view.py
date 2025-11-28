from store.services.coupon_service import CouponService
from store.serializers.admin_serializer import AnalyticsSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from store.services.analytics_service import AnalyticsService
from utils.response_utils import success, error


@extend_schema(tags=["Admin"])
class AnalyticsView(APIView):
    """
    Returns global analytics of the store
    """
    @extend_schema(
        responses={
            200: AnalyticsSerializer
        },
        summary="Get store analytics",
        description="Returns store-wide metrics including total orders, items purchased, discounts, and coupon history."
    )
    def get(self, request):
        stats = AnalyticsService.get_stats()
        return success(data=stats)


@extend_schema(tags=["Admin"])
class GenerateCouponView(APIView):

    @extend_schema(
        responses={200: None},
        summary="Generate discount coupon",
        description="Generates a new 10% discount coupon if nth order milestone is reached."
    )
    def post(self, request):
        coupon, err = CouponService.generate()

        if err:
            return error(err, 400)

        return success(
            {"message": "Coupon generated successfully.", "coupon": coupon}
        )
