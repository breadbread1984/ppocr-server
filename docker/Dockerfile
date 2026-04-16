FROM nvidia/cuda:13.0.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN sed -i "s://archive.ubuntu.com://mirrors.aliyun.com:g" /etc/apt/sources.list
RUN sed -i "s://security.ubuntu.com://mirrors.aliyun.com:g" /etc/apt/sources.list

RUN apt update && apt install -y software-properties-common libgl1

RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt install python3.12 python3.12-venv python3.12-dev wget -y

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py --break-system-packages && \
    rm get-pip.py && \
    rm -rf /var/lib/apt/lists/*

RUN python3.12 -m pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY . .

RUN rm -rf .venv

RUN python3.12 -m uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

