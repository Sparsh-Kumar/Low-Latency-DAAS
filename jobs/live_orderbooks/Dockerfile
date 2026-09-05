FROM python:3.12-slim

WORKDIR /home/source

RUN useradd --create-home appuser \
    && pip install --no-cache-dir uv

COPY libs ./libs
COPY config ./config

COPY jobs/live_orderbooks/pyproject.toml ./jobs/live_orderbooks/pyproject.toml
COPY jobs/live_orderbooks/uv.lock ./jobs/live_orderbooks/uv.lock

RUN uv sync \
    --project jobs/live_orderbooks \
    --locked \
    --no-dev \
    --no-cache

COPY jobs/live_orderbooks ./jobs/live_orderbooks

ENV VIRTUAL_ENV=/home/source/jobs/live_orderbooks/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R appuser:appuser /home/source

USER appuser

CMD ["python", "jobs/live_orderbooks/orderbooks/job.py"]

