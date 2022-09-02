import re


def _clean(content: str):
    content = re.sub('<em>', '', content)
    content = re.sub('<b>', '', content)
    content = re.sub('</b>', '', content)
    content = re.sub('</em>', '', content)
    content = re.sub('<strong>', '', content)
    content = re.sub('</strong>', '', content)
    content = re.sub('<wbr>', '', content)
    content = re.sub('</wbr>', '', content)
    for x in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
        content = content.replace(x, ' ')
    return content


def extract_email(target: str, content: str):
    tmp_email = re.findall(r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + r'[a-zA-Z0-9.-]*' + target, _clean(str(content)))
    email_list = []
    for email in tmp_email:
        if email not in email_list and email.split('@')[0] not in ('"', "'"):
            # 测试功能
            if 'www' in email or '+' in email or '-' in email or ',' in email:
                continue
            email_list.append(email)
    return email_list


def extract_google(target: str, content: str):  # %2522 -> 双引号  %22 -> 单引号  %40 -> @
    email_list = []
    new_content = content.replace('@<em class="qkunPe">', '@')
    result = extract_email(target, new_content)
    for mail in result:
        if '2522' in mail or '22' in mail or '40' in mail:
            continue
        email_list.append(mail)
    return email_list
