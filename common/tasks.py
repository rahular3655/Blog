from typing import Union

import dramatiq
from django.core.mail import send_mail as base_send_email
from django.utils.html import strip_tags
from sentry_sdk import capture_exception


@dramatiq.actor
def send_email(from_email: str, to_email: Union[list, str], subject: str, message: str, attachments=None):
    if not type(to_email) in [str, list]:
        raise Exception('To email must either be a list or single email')
    try:
        base_send_email(
            subject=subject,
            message=strip_tags(message),
            from_email=from_email,
            recipient_list=[to_email] if isinstance(to_email, str) else to_email,
            html_message=message
        )
    except Exception as e:
        capture_exception(e)
