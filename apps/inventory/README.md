# Inventory Django Application

A simple Django application for managing electrical components.

## Features

- Component management (name, description, UUID-based IDs)
- Django admin interface
- RESTful architecture ready

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## Docker Build

Build the Docker image:
```bash
docker build -t inventory:latest .
```

Run locally with Docker:
```bash
docker run -p 8000:8000 inventory:latest
```

## Kubernetes Deployment

The application is configured to be deployed on K3S using ArgoCD.

### Prerequisites

- K3S cluster running
- ArgoCD installed and configured
- Container registry access (ghcr.io/marcoplaisier/inventory)

### Manifests

All Kubernetes manifests are located in `/manifests/apps/inventory/`:

- `namespace.yaml` - Creates the inventory namespace
- `secret.yaml` - Contains the Django SECRET_KEY
- `deployment.yaml` - Deployment with 2 replicas
- `service.yaml` - ClusterIP service on port 80
- `ingress.yaml` - Ingress for inventory.homelab.internal

### Environment Variables

The following environment variables can be configured:

- `DEBUG` - Set to "True" for debug mode (default: "False")
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `SECRET_KEY` - Django secret key (stored in Kubernetes secret)
- `DB_ENGINE` - Database engine (default: sqlite3)
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port

### Access

Once deployed, the application will be accessible at:
- http://inventory.homelab.internal
- Admin interface: http://inventory.homelab.internal/admin/
- Components API: http://inventory.homelab.internal/components/

## Building and Pushing to Registry

```bash
# Build the image
docker build -t ghcr.io/marcoplaisier/inventory:latest apps/inventory/

# Push to registry
docker push ghcr.io/marcoplaisier/inventory:latest
```

## Production Considerations

1. Change the SECRET_KEY in `manifests/apps/inventory/secret.yaml`
2. Consider using PostgreSQL instead of SQLite for production
3. Set up persistent volume for database if using SQLite
4. Configure proper ALLOWED_HOSTS
5. Set DEBUG to False
6. Configure proper logging
7. Set up database backups
