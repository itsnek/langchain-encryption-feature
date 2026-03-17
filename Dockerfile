# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /src

COPY . /src

ENV PYTHONPATH="/src/libs/langchain"

WORKDIR /src/libs/langchain

# Install dependencies
RUN pip install --no-cache-dir -r /src/libs/langchain/requirements.txt

ENTRYPOINT [ "python" ]
