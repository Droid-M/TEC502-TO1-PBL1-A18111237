import requests;
from helpers import file

BASE_URL = file.env("API_URL")

def is_success(response):
    return response.status_code >= 100 or response.status_code < 400

def get(endpoint, headers, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers)

def post(endpoint, headers, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers)
