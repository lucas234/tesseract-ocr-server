# auther：Liul8
# date：2020/7/27 15:01
# tools：PyCharm
# Python：3.7.7
from flask import Flask, request, jsonify
from pytesseract import pytesseract
from PIL import Image
import os
import urllib.request

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_blackwhite_image(picture_name, threshold=160):
    """图片处理成黑白色"""
    table = [0 if _ < threshold else 1 for _ in range(256)]
    image = Image.open(picture_name)
    imgry = image.convert('L')
    out = imgry.point(table, '1')
    return out


def download_image(url):
    files = 'images'
    try:
        if not os.path.exists(files):
            os.makedirs(files)  # 如果没有这个path则直接创建
        image_path = os.path.join(files, "validate_code.jpg")
        # 利用urllib.request.urltrieve方法下载图片
        urllib.request.urlretrieve(url, filename=image_path)
        return image_path
    except IOError as e:
        print(1, e)
        return False
    except Exception as e:
        print(2, e)
        return False


@app.route("/validate-code-recognition", methods=['POST'])
def validate_code_recognition():
    flag = request.form.get("flag", True)
    image = request.files.get("image", None)
    lang = request.form.get("lang", "eng")
    oem = request.form.get("oem", "1")
    psm = request.form.get("psm", "3")
    url = request.form.get("url", None)
    config = f"-l {lang} --oem {oem} --psm {psm}"
    if not image and not url:
        return jsonify({"msg": "image file don`t exist!", "code": 0}), 400
    if image:
        filename = image.filename
    else:
        filename = download_image(url)
        image = filename
    if not allowed_file(filename):
        return jsonify({"msg": f"Allowed file types are: {ALLOWED_EXTENSIONS}", "code": 0}), 400

    if flag:
        image = get_blackwhite_image(image)
    else:
        image = Image.open(image)
    text = pytesseract.image_to_string(image, config=config)
    return jsonify({"code": 1, "msg": "success", "data": {"text": text}}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
