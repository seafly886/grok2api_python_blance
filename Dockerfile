FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests curl_cffi werkzeug loguru 

# 创建/data目录并设置权限
RUN mkdir -p /data && chmod 777 /data
# 删除现有的token文件（如果存在）
# RUN if [ -f /data/token_status.json ]; then rm -f /data/token_status.json; fi

VOLUME ["/data"]

COPY . .

ENV PORT=8698
EXPOSE 8698

CMD ["python", "app.py"]