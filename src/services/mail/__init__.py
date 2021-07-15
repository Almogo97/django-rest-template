from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_rq import job

DEFAULT_CONTEXT = {
    'app_name': 'Django Rest Template',
    'contact_mail': 'contact@test.com'
}


@job
def _send_email(*args, **kwargs):
    send_mail(*args, **kwargs)


def send_email(subject, message, from_email, recipient_list,
               fail_silently=False, auth_user=None, auth_password=None,
               connection=None, html_message=None):
    """
    Easy wrapper for sending a single message, asynchronously, to a recipient list.
    All members of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.
    """

    _send_email.delay(subject, message, from_email, recipient_list,
                      fail_silently, auth_user, auth_password,
                      connection, html_message)


def send_templated_email(subject, from_email, recipient_list, template,
                         fail_silently=False, auth_user=None, auth_password=None,
                         connection=None, context=None):
    """
    Wrapper for send_email that gets the content of the message from a predefined template
    """
    context = DEFAULT_CONTEXT | context if context else DEFAULT_CONTEXT

    message, html_message = _get_rendered_templates(template, context)

    _send_email.delay(subject, message, from_email, recipient_list,
                      fail_silently, auth_user, auth_password,
                      connection, html_message)


def _get_rendered_template(template, extension, context):
    return render_to_string(f'mail/{template}/{template}.{extension}', context)


def _get_rendered_templates(template, context):
    return _get_rendered_template(template, 'txt', context), \
        _get_rendered_template(template, 'html', context)
