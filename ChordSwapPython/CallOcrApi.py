import uuid
import json
import time
import requests

def call_ocr_api(image_path, api_url, secret_key):
    with open(image_path, 'rb') as image_file:
        files = [('file', image_file)]
        request_json = {
            'images': [{'format': 'jpg', 'name': 'demo'}],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        headers = {'X-OCR-SECRET': secret_key}
        
        response = requests.post(api_url, headers=headers, data=payload, files=files)
        return response.json()
