FROM python:3.13-slim
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Install dependencies
COPY requirements.txt ./
RUN pip install --root-user-action=ignore -r requirements.txt --no-cache-dir

# Copy application code
COPY . .

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput

# Change ownership to appuser
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "inventory.wsgi:application"]
