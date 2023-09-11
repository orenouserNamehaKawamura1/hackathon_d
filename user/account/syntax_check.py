import re
import dns.resolver


def syntax_check(mail):
    match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', mail)
    if match is None:
        return False

    mail_domain = re.search("(.*)(@)(.*)", mail).group(3)
    try:
        records = dns.resolver.query(mail_domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        print(mxRecord)
        return True
    except Exception as e:
        return False


def validate_password(pas):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    if re.match(pattern, pas):
        return True
    else:
        return False
