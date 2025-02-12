# 使用 Python 3.10.16 作为基础镜像
FROM python:3.10.16

# 在容器内创建 /home/code 目录
RUN mkdir /home/code

# 设置工作目录为 /home/code
WORKDIR /home/code

# 将本地的 index.py 文件复制到容器内的 /home/code 目录
ADD index.py  /home/code/index.py

# 将本地的 requirements.txt 文件复制到容器内的 /home/code 目录
ADD requirements.txt  /home/code/requirements.txt

ADD download_model.py  /home/code/download_model.py


# 安装 requirements.txt 中指定的 Python 依赖
RUN pip install -r /home/code/requirements.txt


RUN python download_model.py

# 暴露端口 9000
EXPOSE 80

# 容器启动时执行 Python 脚本 index.py
CMD ["python", "index.py"]