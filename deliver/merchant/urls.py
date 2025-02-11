from django.urls import path
from .views import Dashboard, OrderDetails, MerchantDashboard, AddCategoryView, DeleteMenuItem, ChangeItemStatusView, AcceptOrderView, DeclineOrderView, MarkNotificationReadView,ChangeOrderStatusView,ViewOrderHistoryView
app_name = 'merchant'
urlpatterns = [
    path('merchant_dashboard/', MerchantDashboard.as_view(), name='merchant_dashboard'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'), 
    path('orders/<int:pk>', OrderDetails.as_view(), name='order-details'), 
    path('add_category/', AddCategoryView.as_view(), name = 'add_category'), 
    path('menu-item/<int:item_id>/delete/', DeleteMenuItem.as_view(), name='delete_menu_item'),
    path('menu-item/<int:item_id>/change-status/', ChangeItemStatusView.as_view(), name='change_item_status'),
    path('order/<int:order_id>/accept/', AcceptOrderView.as_view(), name='accept_order'),
    path('order/<int:order_id>/decline/', DeclineOrderView.as_view(), name='decline_order'),
    path('mark-notification-read/<int:notification_id>/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('orders/<int:pk>/change-status/', ChangeOrderStatusView.as_view(), name='change_order_status'),
    path('order-history/', ViewOrderHistoryView.as_view(), name='view_order_history'),

]