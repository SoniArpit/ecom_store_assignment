from django.urls import path
from .views.admin_view import AnalyticsView, GenerateCouponView
from .views.cart_view import CartView
from .views.checkout_views import CheckoutView

urlpatterns = [
    path("admin/analytics/", AnalyticsView.as_view()),
    path("admin/generate-coupon/", GenerateCouponView.as_view()),
    path("cart/", CartView.as_view()),   # POST + GET
    path("checkout/", CheckoutView.as_view())
]