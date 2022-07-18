from django import template

register = template.Library()


@register.filter(name='get_flat_detail_notification_url')
def get_flat_detail_notification_url(notification, flat_id):
    return notification.get_flat_detail_url(flat_id)
