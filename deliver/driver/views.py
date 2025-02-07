from django.shortcuts import render
from django.views import View 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # validate the request based on 
from customer.models import OrderModel, Message
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone

# Create your views here.
class DriverDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        driver = request.user.profile
        pending_orders = OrderModel.objects.filter(driver=driver).filter(
            Q(status='Under Preparation') | Q(status='Ready for Pickup') | Q(status='Order On the Way'))
        delivered_orders = OrderModel.objects.filter(driver=driver).filter(
            Q(status='Delivered') | Q(status='Completed'))
        # notifications = Message.objects.filter(recipient=driver, is_read=False)
        notifications = Message.objects.filter(recipient=driver, is_read=False).filter(
            Q(order__driver__isnull=True) | Q(order__driver=driver)
        )
        for notification in notifications:
            if notification.order and notification.order.rating:
                notification.show_rating_button = True
            else:
                notification.show_rating_button = False


            if notification.order:
                notification.show_action_buttons = (
                    notification.order.driver is None and 
                    notification.order.status in ['Ready for Pickup', 'Under Preparation']
                )

            else:
                notification.show_action_buttons = False
        context = {
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'notifications': notifications,
            'notifications_count': notifications.count(),
        }
        return render(request, 'driver/driver_dashboard.html', context)
class GetUnreadNotificationsCountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print('Is this called')
        # Get the count of unread notifications
        unread_count = Message.objects.filter(recipient=request.user.profile, is_read=False).count()
        print('unread count ',  unread_count)
        return JsonResponse({'success': True, 'unread_count': unread_count})
    
class ViewRatingDetailView(LoginRequiredMixin, View):
    def post(self, request, notification_id, *args, **kwargs):
        print('view rating CALLED')
        notification = get_object_or_404(Message, pk=notification_id, recipient=request.user.profile)
        notification.is_read = True
        
        notification.save()
        return JsonResponse({'success': True, 'rating': notification.order.rating, 'comment': notification.order.rating_comment})
    
class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(Message, pk=notification_id, recipient=request.user.profile)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    
class MarkOrderDeliveredView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=order_id)
        order.status = 'Delivered'
        order.delivered_at = timezone.now()
        order.save()
        Message.objects.create(
            sender=order.driver,  # The customer who placed the order
            recipient=order.customer,  # The merchant receiving the notification
            order=order,
            message=f"Order #{order.id} has been delivered by {order.driver.user.username}.", 
            requires_action=False
        )
        return redirect('driver:driver_dashboard')
class MarkOrderOnTheWayView(View):
    def post(self, request, order_id, *args, **kwargs):
        # Fetch the order and ensure it's Ready for Pickup
        order = get_object_or_404(OrderModel, pk=order_id, status='Ready for Pickup')

        # Check if the user is authorized to update the status
        if (request.user.profile.role == 'Merchant' and order.merchant == request.user.profile) or \
           (request.user.profile.role == 'Driver' and order.driver == request.user.profile):
            order.status = 'Order On the Way'
            order.save()
        Message.objects.create(
            sender=request.user.profile,
            recipient=order.customer,
            order=order,
            message=f"Your order #{order.id} is now on the way.",
            requires_action=False
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
class AcceptDeliveryView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        driver = request.user.profile
        order = get_object_or_404(OrderModel, pk=order_id)

        # Assign the driver to the order
        order.driver = driver
        order.save()

        # Mark the notification as read
        Message.objects.filter(order=order, recipient=driver).update(is_read=True)
        Message.objects.create(
            sender=driver,  # The customer who placed the order
            recipient=order.merchant,  # The merchant receiving the notification
            order=order,
            message=f"{driver.user.username} has accepted the order #{order.id}"
        )
        return redirect('driver:driver_dashboard')

class DeclineDeliveryView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        driver = request.user.profile
        order = get_object_or_404(OrderModel, pk=order_id)

        # Mark the notification as read
        Message.objects.filter(order=order, recipient=driver).update(is_read=True)

        # Optionally handle declined orders
        # Example: Notify the merchant or make the order available for other drivers

        return redirect('driver:driver_dashboard')