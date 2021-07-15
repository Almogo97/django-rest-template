import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_rq import job

DEFAULT_CONTEXT = {
    'app_name': 'Django Rest Template',
    'contact_mail': 'contact@test.com'
}

TEMPLATES = {
    'test': {
        'subject': 'This is a test mail',
        'path': 'mail/test',
    },
    'welcome': {
        'subject': 'Welcome to the app %(user)s!',
        'path': 'mail/welcome'
    }
}


@job
def _send_email(*args, **kwargs):
    send_mail(*args, **kwargs)


def send_email(subject, message, recipient_list, from_email=None,
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


def send_templated_email(recipient_list, template, subject=None, from_email=None,
                         fail_silently=False, auth_user=None, auth_password=None,
                         connection=None, context=None):
    """
    Wrapper for send_email that gets the content of the message from a predefined template
    """
    template_values = TEMPLATES[template]
    subject = template_values['subject'] if subject is None else subject
    path = template_values['path']

    context = DEFAULT_CONTEXT | context if context else DEFAULT_CONTEXT

    message, html_message = _get_rendered_templates(path, template, context)

    _send_email.delay(subject, message, from_email, recipient_list,
                      fail_silently, auth_user, auth_password,
                      connection, html_message)


def _get_rendered_template(path, extension, context):
    return render_to_string(f'{path}.{extension}', context)


def _get_rendered_templates(path, name, context):
    path = os.path.join(path, name)
    return _get_rendered_template(path, 'txt', context), \
        _get_rendered_template(path, 'html', context)
