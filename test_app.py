# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 00:14:19 2025

@author: a701192
"""

import requests

# 
url = "http://127.0.0.1:8000/analyze/"  #
headers = {
    "Content-Type": "application/json"
}

data = {
    "text": "I love this product, it's amazing!",
    "model": "llama"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.json())  # This prints the sentiment and confidence
else:
    print(f"Error: {response.status_code}, {response.text}")
