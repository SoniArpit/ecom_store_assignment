from django.urls import path
from .views.admin_view import AnalyticsView
urlpatterns = [
    path("analytics/", AnalyticsView.as_view()),
]