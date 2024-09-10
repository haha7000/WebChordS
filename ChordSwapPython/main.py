import CallOcrApi as coa
import cv2
import ImageProcess as ip

if __name__ == "__main__":
    api_url = 'https://qrzccj1y9c.apigw.ntruss.com/custom/v1/22243/60e2b8a7e366adc85128cffa9fb17254e9c8e9e4a73a7b6eac9c819a718987a3/general'
    secret_key = 'ZkhvZFJGUXd2WFRkVWNrWExGc0RXbU9EaVRGYXZuRkc='
    image_path = 'images/upstill.jpg'
    half_steps = 2  # 원하는 반음 조정

    ocr_result = coa.call_ocr_api(image_path, api_url, secret_key)
    processed_img = ip.process_image(image_path, ocr_result, half_steps)

    cv2.imshow("Original Image", cv2.imread(image_path))
    cv2.imshow("Processed Image", processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    