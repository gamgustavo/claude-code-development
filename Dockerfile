FROM public.ecr.aws/docker/library/python:3.12-slim

ARG APP_VERSION=dev
ENV PYTHONUNBUFFERED=1 PORT=8080 APP_VERSION=$APP_VERSION
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Estándar docker.md: no correr como root
RUN useradd --system --uid 10001 appuser
USER appuser

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8080/health')"
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]
