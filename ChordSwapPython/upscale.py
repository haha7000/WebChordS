import cv2
import numpy as np
from cv2 import dnn_superres


def upscale_image(image_path, model_path, output_path):
    # 이미지 불러오기
    image = cv2.imread(image_path)

    # 모델 불러오기
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel('edsr', 3)

    # 이미지 해상도 높이기
    upscaled = sr.upsample(image)

    # 결과 이미지 저장
    cv2.imwrite(output_path, upscaled)


# 예시 사용
image_path = 'images/lowimg.jpg'
model_path = 'model/EDSR_x3.pb'
output_path = 'images/upscaled.jpg'

upscale_image(image_path, model_path, output_path)
