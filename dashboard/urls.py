
from django.urls import path

from dashboard.apis import DashboardStatistics

urlpatterns = [
    path('statistics/', DashboardStatistics.as_view(), name="dashboard-statistics")
]
