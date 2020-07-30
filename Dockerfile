FROM python:3.7-alpine
# 设置阿里云镜像，解决下载失败、速度慢的问题
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add --update --no-cache tesseract-ocr g++ gcc libxslt-dev openssl-dev jpeg-dev zlib-dev
COPY requirements.txt /usr/src/app/
# 设置阿里云镜像，解决下载失败、速度慢的问题
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && pip config set install.trusted-host mirrors.aliyun.com
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
COPY api.py /usr/src/app/
COPY chi_sim.traineddata /usr/share/tessdata/
EXPOSE 5000
CMD ["python", "/usr/src/app/api.py"]