from services.mail import send_templated_email


# TODO convert from itegration test to unit test
class TestSendTemplatedEmail:
    def test_sends_email(self, mailoutbox):
        send_templated_email('subject', ['to@test.com'], 'test', context={'test_value': 'value'})

        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert m.subject == 'subject'
        assert 'This is a simple test value' in m.body
        assert m.to == ['to@test.com']
