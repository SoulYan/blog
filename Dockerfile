FROM openwhisk/python3action
LABEL maintainer="maple7yuan@gmail.com"
COPY . /src
WORKDIR /src
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 8080
CMD ["gunicorn","blog:create_app","-c","./gunicorn.conf.py"]
