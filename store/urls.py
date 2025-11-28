from django.urls import path
from .views.admin_view import AnalyticsView
from .views.cart_view import CartView

urlpatterns = [
    path("analytics/", AnalyticsView.as_view()),
    path("cart/", CartView.as_view()),   # POST + GET
]