# Stage 1: Build dependencies
FROM python:3.12.3-slim AS builder

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.12.3-slim
WORKDIR /usr/src/app

COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000

ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ["uvicorn"]
CMD ["src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]