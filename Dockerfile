FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir flask requests

COPY cloudget/ cloudget/

EXPOSE 9999

CMD ["python", "-m", "cloudget"]
