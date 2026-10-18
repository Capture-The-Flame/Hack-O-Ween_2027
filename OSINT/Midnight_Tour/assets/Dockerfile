# The Midnight Tour - OSINT CTF Challenge
FROM python:3.12-slim

WORKDIR /app

# Standard library only, nothing to pip install
COPY app/app.py .
COPY app/site ./site

# Run as a non-root user
RUN useradd -m ctfuser && chown -R ctfuser:ctfuser /app
USER ctfuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["python", "app.py"]
