FROM python:3.14-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    freetype-dev \
    libpng-dev \
    openblas-dev

RUN pip install --no-cache-dir numpy matplotlib

COPY . /app

CMD ["python3"]
