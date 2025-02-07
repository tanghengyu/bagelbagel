from django.urls import path
from .views import DriverDashboardView, MarkNotificationReadView, AcceptDeliveryView, DeclineDeliveryView, MarkOrderDeliveredView,MarkOrderOnTheWayView, ViewRatingDetailView,GetUnreadNotificationsCountView
app_name = 'driver'
urlpatterns = [
    path('dashboard/', DriverDashboardView.as_view(), name='driver_dashboard'),
    path('mark-notification-read/<int:notification_id>/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('view-rating-detail/<int:notification_id>/', ViewRatingDetailView.as_view(), name='view_rating_detail'),
    path('order/<int:order_id>/accept-delivery/', AcceptDeliveryView.as_view(), name='accept_delivery'),
    path('order/<int:order_id>/decline-delivery/', DeclineDeliveryView.as_view(), name='decline_delivery'),
    path('order/<int:order_id>/mark-delivered', MarkOrderDeliveredView.as_view(), name= 'mark_order_delivered'),
    path('order/<int:order_id>/mark-on-the-way/', MarkOrderOnTheWayView.as_view(), name='mark_order_on_the_way'),
    path('driver/get-unread-notifications-count/', GetUnreadNotificationsCountView.as_view(), name='get_unread_notifications_count'),

]