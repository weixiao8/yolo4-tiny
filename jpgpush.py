# 向管理平台推流
import base64
import json
import os
import time
import requests
import shutil
def ToPush(filename):
    print(filename)
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K) tuhuAndroid 5.24.6',
               'content-type': 'application/json',
               "secretKey": "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"
               }

    f = open(filename, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    url = "http://njdt.njtjy.org.cn:10032/api/intelligentPrediction/save"
    jpgbase64 = "data:image/jpg;base64," + str(ls_f)[2:-1]
    data = {"deviceNo": "MARK-42", "type": "1", "warningNum": "1", "imgBase64": jpgbase64}  # Post请求发送的数据，字典格式
    res = requests.post(url=url, data=json.dumps(data), headers=headers)  # 这里使用post方法，参数和get方法一样
    print(jpgbase64)
    print(res.text)
    response = res.text[8:11]
    f.close()
    if response == "200":
        return 1
    else:
        return 0

if __name__ == '__main__':
    interval = 10
    interval_flag = 0
    while 1:
        if interval_flag == 1:
            for i in range(interval):
                time.sleep(1)
                print("等待{}秒".format(i))
        yearmonthdayfile = time.strftime("%Y_%m_%d", time.localtime())
        jpgpath = yearmonthdayfile + "/"
        if not os.path.exists(jpgpath):
            interval_flag = 0
            print("暂无预警")
            continue
        files = os.listdir(jpgpath)
        if len(files) == 0:
            interval_flag = 0
            print("暂无预警")
            continue
        if len(files) > 0:
            time.sleep(1)
            filename = jpgpath + files[0]
            res = ToPush(filename)
            if res == 0:
                print("图片推流失败")
            if res == 1:
                print("清空剩余的frame")
                path = jpgpath
                for i in os.listdir(path):
                    path_file = os.path.join(path, i)
                    if os.path.isfile(path_file):
                        os.remove(path_file)
                        #time.sleep(2)
                    else:
                        for f in os.listdir(path_file):
                            path_file2 = os.path.join(path_file, f)
                            if os.path.isfile(path_file2):
                                os.remove(path_file2)
            interval_flag = 1

