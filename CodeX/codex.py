import os
import sys
import time
import requests
from urllib import parse

sys.path.append('/mnt/d/Semester 8/Cloud Javadi/HW/HW1/code/')
from Handler.utils.db import DatabaseHandler


def codex_request(filename: str, input_str: str=''):
    if not os.path.exists(filename):
        print(f'{filename} does not exist')
        return {}
    
    CodeX_URL     = "https://api.codex.jaagrav.in"
    
    _, language = os.path.splitext(filename)
    if language:
        language = language[1:]

    source_code = None
    with open(filename, 'r') as f:
        source_code = f.read()

    data = {
        'code': source_code,
        'language': language, 
        'input': input_str
    }

    resp = requests.request(
        method='post', 
        url=CodeX_URL, 
        data=data, 
        headers={
        'content-type': 'application/x-www-form-urlencoded'
        }
    )
    return resp.text

def codex_request_options(source_code: str, language: str, input_str: str = ""):
    CodeX_URL     = "https://api.codex.jaagrav.in"

    data = {
        'code': source_code,
        'language': language, 
        'input': input_str
    }

    resp = requests.request(
        method='post', 
        url=CodeX_URL, 
        data=data, 
        headers={
        'content-type': 'application/x-www-form-urlencoded'
        }
    )
    return resp.text

def codex_request_str(query_str: str):
    CodeX_URL     = "https://api.codex.jaagrav.in"

    resp = requests.request(
        method='post', 
        url=CodeX_URL, 
        data=query_str, 
        headers={
        'content-type': 'application/x-www-form-urlencoded'
        }
    )
    return resp.json()

def send_email(email, txt):
    requests.post(
        "https://api.mailgun.net/v3/sandbox229a2b6ecdce450cadff15749afbb10b.mailgun.org/messages",
        auth=("api", "770ece8c0c5765abbfe05e19dca9488a-81bd92f8-f55b5b26"),
        data={"from": "Execode <postmaster@sandboxaf366ba8f6684a049511c24bd9da549c.mailgun.org>",
              "to": f"<{email}>",
              "subject": "Output of Code",
              "text": f"Hi,\nThe result the code you uploaded is here:\n```\n{txt}\n```"})

def loop():
    with DatabaseHandler() as db_handler:
        conditions_dict = {
            'executed': 0
        }
        rows = db_handler.find_all('JOBS', conditions_dict)
        for row in rows:
            response = codex_request_str(row['job'])
            assignment_dict = {
                'output': response['output'],
                'done': 1
            }
            db_handler.update('RESULTS', {'job_id': row['id']}, assignment_dict)
            db_handler.update('JOBS', {'id': row['id']}, {'executed': 1})
            email_body = ''
            if len(response['error']) > 0:
                db_handler.update('UPLOADS', {'id': row['upload_id']}, {'enable': 1})
                email_body += f'ERROR:\n{response["error"]}'
            else:
                email_body += f'OUTPUT:\n{response["output"]}'

            upload_row = db_handler.find('UPLOADS', row_id=row['upload_id'], column_list=['email'])
            email = upload_row['email']
            send_email(email, email_body)


if __name__ == '__main__':
    # print(codex_request('test.py'))
    # print(codex_request_str(parse.urlencode({'code': 'import os\nprint(os.getcwd())\nprint(3 + 4)', 'language': 'py', 'input': ''})))
    # while(True):
    #     loop()
    #     time.sleep(30)
    send_email('iran.volleyball79@gmail.com', 'hello, I am a test output')