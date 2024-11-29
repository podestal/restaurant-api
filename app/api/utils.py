from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

def send_order_status_email(email, order):
    """Send an order status email to the customer."""
    subject = 'Order Ready Notification'
    context = {'order': order, 'current_year': datetime.now().year,}
    plain_message = f"Hello,\n\nYour order with ID {order.id} is ready for pickup.\n\nThank you for choosing our service!"
    html_message = render_to_string('emails/order_ready.html', context)
    send_mail(
        subject,
        message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[email],
        fail_silently=False,
    )