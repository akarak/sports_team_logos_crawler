ARG PYTHON_VERSION=3.12.1
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY ./requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

ARG OUTPUT_DIR=/output
ARG TASKS_DIR=/tasks

COPY .${TASKS_DIR} ${TASKS_DIR}
RUN mkdir -p ${OUTPUT_DIR}

ENV APP_DIR=/app
ENV OUTPUT_DIR=${OUTPUT_DIR}
ENV TASKS_DIR=${TASKS_DIR}

VOLUME ${OUTPUT_DIR} ${TASKS_DIR}

COPY .$APP_DIR $APP_DIR
WORKDIR $APP_DIR

USER appuser

ENTRYPOINT ["python", "main.py", "--output_dir=/output", "--tasks_dir=/tasks"]
CMD []
