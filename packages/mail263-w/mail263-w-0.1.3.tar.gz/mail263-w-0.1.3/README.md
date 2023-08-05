### demo

```python
import ssl

from client_263 import Mail263Client

if __name__ == '__main__':
    ssl_context = ssl.create_default_context()
    # don't check if certificate hostname doesn't match target hostname
    ssl_context.check_hostname = False
    # don't check if the certificate is trusted by a certificate authority
    ssl_context.verify_mode = ssl.CERT_NONE

    with Mail263Client('imap.263.net', 'your_email', 'your_password', ssl_context=ssl_context) as client:
        # rule_dict = {
        #     'rule_name': '规则标题',
        #     'sender': {'cond': 'include', 'text': sender_email},
        #     'recipient': {'cond': 'not include', 'text': recipient_email},
        #     'subject': {'cond': 'include', 'text': '估值表'},
        #     'size': {'cond': '>=', 'num': 20},
        #     'action': {'type': 'move', 'folder_name': 'TEST'}
        # }
        # resq = client.set_mail_rule(rule_dict)
        # resq = client.create_263mail_folder(folder_name)
        # mail_list = cliend.get_mails(folder_name,status='UNSEEN')[0]

```