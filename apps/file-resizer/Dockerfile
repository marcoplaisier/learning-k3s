FROM python:3.13-slim
WORKDIR /file-resizer

RUN adduser --disabled-password --gecos '' appuser

COPY requirements.txt ./
RUN pip install --root-user-action=ignore -r requirements.txt
COPY . .
RUN chown -R appuser:appuser /file-resizer

USER appuser
EXPOSE 5000
CMD ["python", "main.py"]