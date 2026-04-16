FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN apt update

RUN apt install -y curl

RUN curl -LsSf https://astral.sh/uv/install.sh | \
    UV_INSTALL_DIR=/usr/local/bin sh && \
    ls -la /usr/local/bin/uv && \
    /usr/local/bin/uv --version

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

RUN rm -rf .venv

RUN uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

RUN uv pip install paddlepaddle-gpu==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu128/

