from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        today = timezone.now().date()
        value = timezone.localtime(value)
        if value.date() == today:
            return f"Today at {value.strftime("%I:%M %p")}"
        elif value.date() == today.replace(day=today.day - 1):
            return f"Yesterday at {value.strftime("%I:%M %p")}"
        else:
            return f'{value.date().strftime("%B %d, %Y")}, {value.strftime("%I:%M %p")}'
    else:
        return 'No login record available!'