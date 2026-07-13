FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pytest pandas requests pydantic
# No CMD, this image is used for one-off runs by ControlAgent
