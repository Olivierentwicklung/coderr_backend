from django.urls import path

from orders_app.api.views import OrderDetailView, OrderListCreateView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
