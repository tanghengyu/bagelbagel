from django.urls import path
from .views import DriverDashboardView, MarkNotificationReadView, AcceptDeliveryView, DeclineDeliveryView, MarkOrderDeliveredView,MarkOrderOnTheWayView
app_name = 'driver'
urlpatterns = [
    path('dashboard/', DriverDashboardView.as_view(), name='driver_dashboard'),
    path('mark-notification-read/<int:notification_id>/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('order/<int:order_id>/accept-delivery/', AcceptDeliveryView.as_view(), name='accept_delivery'),
    path('order/<int:order_id>/decline-delivery/', DeclineDeliveryView.as_view(), name='decline_delivery'),
    path('order/<int:order_id>/mark-delivered', MarkOrderDeliveredView.as_view(), name= 'mark_order_delivered'),
    path('order/<int:order_id>/mark-on-the-way/', MarkOrderOnTheWayView.as_view(), name='mark_order_on_the_way'),

]