FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext curl && \
    rm -rf /var/lib/apt/lists/* \
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-root
COPY entrypoint.sh ./
COPY src/ .

CMD ["/bin/bash", "entrypoint.sh"]