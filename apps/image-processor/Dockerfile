FROM python:3.13-slim
WORKDIR /image-processor

RUN adduser --disabled-password --gecos '' appuser

COPY requirements.txt ./
RUN pip install --root-user-action=ignore -r requirements.txt --no-cache-dir
COPY . .
RUN chown -R appuser:appuser /image-processor

USER appuser
EXPOSE 5000
CMD ["python", "main.py"]