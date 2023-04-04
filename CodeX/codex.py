import os
import requests


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

def codex_request_str(source_code: str, language: str, input_str: str = ""):
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

print(codex_request_str('import os\nprint(os.getcwd())\nprint(3 + 4)', language='py'))