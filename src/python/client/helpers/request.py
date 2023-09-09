import requests;
from helpers import file

BASE_URL = file.env("API_URL")

def is_success(response):
    return response.status_code >= 100 and response.status_code < 400

def get(endpoint, headers, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers)

def post(endpoint, headers, body = {}, query = {}):
    return requests.post(BASE_URL + "/" + endpoint, json = body, params = query, headers = headers)

def render_response_message(response):
    message = response.json().get("message")
    if message:
        print(message)
    else:
        print("Sucesso na requisição!" if is_success(response) else "Falha na requisição")
    if (response.status_code == 422):
        errors = response.json().get('errors', [])
        if isinstance(errors, dict):
            for i in errors:
                print(f"{i}: {errors[i]}")
        elif isinstance(errors, list):
            for i in errors:
                print(i)
    
