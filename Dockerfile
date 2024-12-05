FROM python:3.11-slim

RUN apt-get update && apt-get install -y libmariadb3 libmariadb-dev gcc

# Install pipx
RUN python3 -m pip install --upgrade pipx

# Set environment variables for pipx
ENV PIPX_BIN_DIR=/opt/pipx/bin
ENV PIPX_HOME=/opt/pipx/home
ENV PATH=${PIPX_BIN_DIR}:${PATH}

# Set the working directory:
RUN mkdir /app
WORKDIR /app

# Copy in the python prereq files:
COPY ./pyproject.toml ./poetry.lock /app/

# Install packages using pipx
RUN pipx install black
RUN pipx install isort

# Install poetry
RUN pipx install poetry && \
    poetry lock --no-update

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Expose the port that the app runs on:
EXPOSE 5000

# Copy in the rest of the files:
COPY . /app

# ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD ["poetry", "run", "/root/.cache/pypoetry/virtualenvs/azure-web-app-vfs-9TtSrW0h-py3.11/bin/gunicorn", "wsgi:app", "-b", "0.0.0.0:5000", "--workers=4"]