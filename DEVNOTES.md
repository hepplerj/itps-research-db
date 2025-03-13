## DEVNOTES

### Create a backup

```bash
docker-compose exec db pg_dump -U postgres your_db_name > backup.sql
```

### Restore a backup

```bash
docker-compose exec -T db psql -U postgres your_db_name < backup.sql
```

# Dependencies

## Poetry to Requirements.txt

When updating dependencies with Poetry, you'll need to update requirements.txt for Docker builds:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls
```

# Django ITPS Research Deployment Guide

This document outlines the steps to deploy the ITPS Research Django application using Docker in a production environment. The site is currently hosted on Reclaim Cloud.

## Prerequisites

- Ubuntu server and nginx load balancer
- Docker and Docker Compose installed
- Domain/subdomain configured to point to the server (e.g., research.theitsp.org)

## Project Structure

```txt
itps_research/
├── app/                    # Django project code
├── nginx/                  # Nginx configuration
│   ├── Dockerfile          # Nginx Dockerfile
│   └── nginx.conf          # Nginx configuration
├── .env.prod               # Production environment variables for Django
├── .env.prod-db            # Production environment variables for PostgreSQL
├── docker-compose.prod.yml # Production Docker Compose configuration
└── DEVNOTES.md             # This file
```

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/hepplerj/itps-research-db /opt/itps_research
cd /opt/itps_research
```

### 2. Create Environment Files

Create `.env.prod`:

```txt
DEBUG=0
DJANGO_SECRET_KEY=your_generated_secret_key  # Generate with: python -c "import secrets; print(secrets.token_urlsafe(50))"
DJANGO_ALLOWED_HOSTS=research.theitsp.org,your_server_ip,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=https://research.theitsp.org
DB_HOST=db
DB_NAME=itps_research
DB_USER=your_prod_user
DB_PASS=your_secure_password
DB_PORT=5432

# HTTPS settings for working with reverse proxy
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=31536000 # one year
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True
```

Create `.env.prod-db`:

```txt
POSTGRES_USER=your_prod_user # must match DB_USER
POSTGRES_PASSWORD=your_secure_password # must match DB_PASS
POSTGRES_DB=itps_research
```

### 3. Nginx Configuration

Create nginx/Dockerfile:

```dockerfile
FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

Create nginx/nginx.conf:

```nginx
upstream itps_research {
    server web:8000;
}

server {
    listen 80;
    server_name research.theitsp.org;

    location /staticfiles/ {
        alias /home/app/web/staticfiles/;
    }

    location /mediafiles/ {
        alias /home/app/web/mediafiles/;
    }

    location / {
        proxy_pass http://itps_research;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

## Deployment

### 1. Build and Start Containers

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. Run Migrations

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### 3. Collect Static Files

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

### 4. Create Superuser

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 5. Load Fixtures

Copy fixture files to the container:

```bash
docker cp users.json container_name:/home/app/web/fixtures/
```

Load the fixtures:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata fixtures/users.json
```

For content type conflicts, use:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata fixtures/your_data.json --exclude=contenttypes
```

Then load in the current data fixture:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata data-update
```

## Maintenance Tasks

### Check Container Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Logs

```bash
docker-compose -f docker-compose.prod.yml logs web  # Django logs
docker-compose -f docker-compose.prod.yml logs db   # Database logs
docker-compose -f docker-compose.prod.yml logs nginx # Nginx logs
```

### Update Application

After making changes to the code:

```bash
git pull  # Pull the latest changes
docker-compose -f docker-compose.prod.yml up -d --build web  # Rebuild web container
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate  # Apply migrations if needed
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input  # Update static files
```

### Database Backup

Create a backup script (backup_db.sh):

```bash
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/opt/itps_research/backups"
CONTAINER_NAME="itps_research_db_1"  # Check your actual container name

mkdir -p $BACKUP_DIR
docker exec $CONTAINER_NAME pg_dump -U your_prod_user -d itps_research > $BACKUP_DIR/db_backup_$TIMESTAMP.sql
```

Make it executable and run it:

```bash
chmod +x backup_db.sh
./backup_db.sh
```

### Database Restore

```bash
cat backup_file.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U your_prod_user -d itps_research
```

### Clean Up Unused Resources

Remove unused containers, networks, images, and volumes:

```bash
docker system prune -a  # Remove all unused containers, networks, and images
docker volume prune     # Remove all unused volumes
```

To remove specific volumes:

```bash
docker volume rm volume_name
```

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
