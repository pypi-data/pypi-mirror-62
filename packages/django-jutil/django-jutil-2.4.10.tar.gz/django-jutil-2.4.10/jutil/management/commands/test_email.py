import os

from django.conf import settings
from django.core.management.base import CommandParser
from django.utils.timezone import now
from jutil.command import SafeCommand
from jutil.email import send_email


class Command(SafeCommand):
    help = 'Send test email with attachment'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('email', type=str)
        parser.add_argument('--cc', type=str)
        parser.add_argument('--bcc', type=str)
        parser.add_argument('--attach', type=str, nargs='*')

    def do(self, *args, **kw):
        files = kw['attach'] if kw['attach'] else []
        if not files:
            files.append(os.path.join(settings.BASE_DIR, 'data/attachment.jpg'))
        subject = 'hello ' + now().isoformat()
        text = 'body text'
        html = '<h1>html text</h1><p><a href="https://kajala.com/">Kajala Group Ltd.</a></p>'
        sender = '"Kajala Group Asiakaspalvelu" <asiakaspalvelu@kajala.com>'
        res = send_email(kw['email'], subject, text, html, sender, files, bcc_recipients=kw['bcc'], cc_recipients=kw['cc'])
        print('send_email returned', res)
