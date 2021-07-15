from io import StringIO
from django.core.management import call_command

class TestSendMail:
    def test_sends_mail(self, mock_send_templated_email):
        out = StringIO()
        call_command('sendmail', 'test@test.com', stdout=out, template='welcome')
        assert 'Email sent!' in out.getvalue()
        mock_send_templated_email.assert_called_once_with(
            'test', None, ['test@test.com'], 'welcome', fail_silently=False
        )
