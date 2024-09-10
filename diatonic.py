import os
import cv2
import uuid
import json
import time
import requests
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def call_ocr_api(image_path, api_url, secret_key):
    try:
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
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
            return response.json()
    except Exception as e:
        logging.error(f"OCR API 호출 중 오류 발생: {e}")
        return None

def modify_text(text):
    replaced_text = text.replace("t", "#")
    replaced_text = replaced_text.replace("&", "#")
    return replaced_text

def transpose_chord(chord, half_steps):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    root_note = chord[0]
    root_index = notes.index(root_note)
    
    new_index = (root_index + half_steps) % 12
    return notes[new_index] + chord[1:]

def estimate_key(chords):
    # 각 키에 해당하는 다이아토닉 코드 세트 정의
    diatonic_chords = {
        'C': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'],
        'G': ['G', 'Am', 'Bm', 'C', 'D', 'Em', 'F#dim'],
        'D': ['D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#dim'],
        'A': ['A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#dim'],
        'E': ['E', 'F#m', 'G#m', 'A', 'B', 'C#m', 'D#dim'],
        'B': ['B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#dim'],
        'F#': ['F#', 'G#m', 'A#m', 'B', 'C#', 'D#m', 'E#dim'],
        'Db': ['Db', 'Ebm', 'Fm', 'Gb', 'Ab', 'Bbm', 'Cdim'],
        'Ab': ['Ab', 'Bbm', 'Cm', 'Db', 'Eb', 'Fm', 'Gdim'],
        'Eb': ['Eb', 'Fm', 'Gm', 'Ab', 'Bb', 'Cm', 'Ddim'],
        'Bb': ['Bb', 'Cm', 'Dm', 'Eb', 'F', 'Gm', 'Adim'],
        'F': ['F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim']
    }

    # 각 키와의 일치하는 코드 빈도 계산
    key_matches = {key: 0 for key in diatonic_chords}

    for chord in chords:
        for key, diatonic_set in diatonic_chords.items():
            if chord in diatonic_set:
                key_matches[key] += 1

    # 일치하는 코드가 가장 많은 키 추정
    estimated_key = max(key_matches, key=key_matches.get)
    return estimated_key

def main(image_path, half_steps=0):
    api_url = 'https://qrzccj1y9c.apigw.ntruss.com/custom/v1/22243/60e2b8a7e366adc85128cffa9fb17254e9c8e9e4a73a7b6eac9c819a718987a3/general'
    secret_key = 'ZkhvZFJGUXd2WFRkVWNrWExGc0RXbU9EaVRGYXZuRkc='

    ocr_result = call_ocr_api(image_path, api_url, secret_key)
    if ocr_result is None:
        logging.error('OCR 처리 중 오류가 발생했습니다.')
        return

    chords = []
    for field in ocr_result['images'][0]['fields']:
        text = field['inferText']
        first_char = text[0] if len(text) > 0 else ''

        if first_char.isupper() and first_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            chords.append(text)

    key = estimate_key(chords)
    logging.info(f"추정된 키: {key}")
    return key

if __name__ == "__main__":
    # 테스트할 이미지 경로와 반음 이동 값 설정
    test_image_path = '/Users/gimdonghun/Downloads/el.png'
    half_steps = 0  # 원하는 반음 이동 값

    estimated_key = main(test_image_path, half_steps)
    if estimated_key:
        print(f"추정된 키: {estimated_key}")
    else:
        print("키 추정에 실패했습니다.")
