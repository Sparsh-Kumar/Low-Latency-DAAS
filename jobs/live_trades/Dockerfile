FROM python:3.12-slim

WORKDIR /home/source

RUN useradd --create-home appuser \
    && pip install --no-cache-dir uv

COPY libs ./libs
COPY config ./config

COPY jobs/live_trades/pyproject.toml ./jobs/live_trades/pyproject.toml
COPY jobs/live_trades/uv.lock ./jobs/live_trades/uv.lock

RUN uv sync \
    --project jobs/live_trades \
    --locked \
    --no-dev \
    --no-cache

COPY jobs/live_trades ./jobs/live_trades

ENV VIRTUAL_ENV=/home/source/jobs/live_trades/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R appuser:appuser /home/source

USER appuser

CMD ["python", "jobs/live_trades/trades/job.py"]


