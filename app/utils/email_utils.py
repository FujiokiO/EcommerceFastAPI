from app.api.v1.auth_route import account


def send_verification_email(email_address: str, verification_code: str):
    # 创建邮件内容
    m = account.new_message()
    m.to.add(email_address)
    m.subject = 'Verification Code'
    m.body = f'Your verification code is: {verification_code}'
    m.send()
    return True
