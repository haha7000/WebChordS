import cv2
import numpy as np

# 이미지 불러오기
image = cv2.imread('images/still.jpg')

# 이미지를 회색조로 변환

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Otsu 이진화 수행
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

# 결과 확인
cv2.imshow('Original Image', image)
cv2.imshow('Binary Image', binary_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

