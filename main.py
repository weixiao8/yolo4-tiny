import os
import time

import cv2
import numpy as np
from flask import Flask, render_template, Response



class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # def get_frame(self):
    #     # success, image = self.video.read()
    #
    #     # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
    #     ret, jpeg = cv2.imencode('.jpg', image)
    #     return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')


def gen():
    count_flag = 0
    while True:
        time.sleep(0.19)
        if count_flag < 2:
            filename = "frame_out/"+str(count_flag)+"_out.npy"
            try:
                image = np.load(filename)
            except:
                while not os.path.exists(filename):
                    pass
                image = np.load(filename)
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            count_flag += 1
        if count_flag == 2:
            count_flag = 0
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
        return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/update')  # 更新模型
def video_feed():
        return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5000)