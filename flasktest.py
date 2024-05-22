import base64
import logging
import io

import numpy as np
from flask import Flask, Response, request, json, jsonify
from PIL import Image
import cv2
import camera2
import os

app = Flask(__name__)
@app.route('/stream', methods=['POST'])
def stream():
    try:
        # file = request.files['image']
        # # JSON 데이터 수신
        data = request.get_json()
        encoded_image_data = data['image']
        decoded_image_data = base64.b64decode(encoded_image_data)

        # temp_image_path = 'temp_image.png'
        # with open(temp_image_path, 'wb') as file:
        #     file.write(decoded_image_data)
        #     print(f"Saved image size: {os.path.getsize(temp_image_path)} bytes")

        image = Image.open(io.BytesIO(decoded_image_data))
        image = np.array(image)
        # image= cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        processed_frame = camera2.process_stream(image)

        # 결과 반환
        response = {
            "result": "카메라 실행이 완료됐습니다",
            "data": processed_frame
        }
        return jsonify(response)
    except Exception as e:
        # 오류가 발생할 경우 오류 메시지와 함께 500 응답 반환
        logging.error(f"Error processing image: {e}")
        return jsonify({'error': str(e)}), 500

# @app.route('/stream', methods=['POST'])
# def stream():
#     # 프레임 받아 처리
#     frame_data = request.data
#     # if not encoded_data:
#     #     return jsonify({'error': 'No data provided'}), 400
#     # decoded_data = base64.b64decode(encoded_data)
#     # logging.info("Data decoded successfully")
#     np_arr= np.frombuffer(frame_data,np.uint8)
#     # image = Image.open(io.BytesIO(decoded_data))
#     image = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)
#     # image_data = np.array(image)
#     # image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
#     # logging.info("Image loaded and color converted")
#
#     # 객체 감지 , 손 인식
#     processed_frame = camera2.process_stream(image)
#     # 결과 반환
#     response = {
#         "result": "카메라 실행이 완료됐습니다",
#         "data": processed_frame
#     }
#     return jsonify(response)



@app.route("/test", methods=['GET'])
def versionCheck():
    print("받은 Json 데이터 ")
    response = {
        "result": "ok"
    }
    return jsonify(response)

@app.route('/video', methods=['POST'])
def receive_image():
    try:
        image_data = request.get_data()
        # 여기서 image_data를 사용하여 이미지 처리를 수행할 수 있습니다.

        # 연결 확인 응답을 보냅니다.
        return '연결됨', 200
    except Exception as e:
        return f'에러: {e}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)