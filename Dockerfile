FROM python:3.12-bookworm

# Environment
ENV BLE_BLUELEAKS_PATH=/data/blueleaks
ENV BLE_DATABASES_PATH=/data/databases
ENV BLE_STRUCTURES_PATH=/data/structures

# Copy the built-in and the default structures
RUN mkdir -p /var/blueleaks-explorer/structures-builtin
COPY structures-builtin/* /var/blueleaks-explorer/structures-builtin
RUN mkdir -p /var/blueleaks-explorer/structures-default
COPY structures-default/* /var/blueleaks-explorer/structures-default

# Install updates in container
RUN DEBIAN_FRONTEND=noninteractive && \
    export DEBIAN_FRONTEND && \
    apt-get update && \
    apt-get upgrade --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js from NodeSource repository
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install nodejs -y && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

WORKDIR /app

# Install python dependencies
COPY src/pyproject.toml .
COPY src/poetry.lock .
RUN poetry install --no-root

# Copy the frontend
RUN mkdir frontend
COPY src/frontend/package.json frontend
COPY src/frontend/package-lock.json frontend

# Install node dependencies
RUN cd frontend && npm install

# Copy everything else
COPY src .

# Build the frontend
RUN cd frontend && npm install
RUN cd frontend && npm run build
# RUN cd frontend && npm run build -m development

# Execute
EXPOSE 80
ENV FLASK_APP=app
CMD ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "80"]