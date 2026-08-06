FROM python:3.12-slim

WORKDIR /home/source

RUN useradd --create-home appuser \
  && pip install --no-cache-dir uv

COPY libs ./libs
COPY config ./config
COPY jobs/live_tickers/pyproject.toml ./jobs/live_tickers/pyproject.toml

RUN uv sync \
  --project jobs/live_tickers \
  --no-dev \
  --no-cache

COPY jobs/live_tickers ./jobs/live_tickers

ENV VIRTUAL_ENV=/home/source/jobs/live_tickers/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R appuser:appuser /home/source

USER appuser

CMD ["python", "jobs/live_tickers/job.py"]
