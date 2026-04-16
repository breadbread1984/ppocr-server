FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN apt update && apt install python3 python3-pip -y

RUN python3 -m pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY . .

RUN rm -rf .venv

RUN python3 -m uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

RUN python3 -m uv pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu128/

