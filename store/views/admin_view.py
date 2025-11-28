from store.serializers.admin_serializer import AnalyticsSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from store.services.analytics_service import AnalyticsService
from utils.response_utils import success


@extend_schema(tags=["Store Analytics"])
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
