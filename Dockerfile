FROM python:3.10-bullseye

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

# Install nodejs
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.1/install.sh | bash && \
    . /root/.bashrc && \
    sleep 1 && \
    nvm install 18.2.0 && \
    ln -s /root/.nvm/versions/node/v18.2.0/bin/node /usr/local/bin/node && \
    ln -s /root/.nvm/versions/node/v18.2.0/bin/npm /usr/local/bin/npm && \
    ln -s /root/.nvm/versions/node/v18.2.0/bin/npx /usr/local/bin/npx

# Install poetry
RUN pip install poetry

# Copy the code
WORKDIR /app

# Install python dependencies
COPY src/pyproject.toml .
COPY src/poetry.lock .
RUN poetry install

# Copy the frontend
RUN mkdir frontend
COPY src/frontend/package.json frontend
COPY src/frontend/package-lock.json frontend

# Install node dependencies
RUN cd frontend && npm install

# Copy everything else
COPY src .

# Build the frontend
RUN cd frontend && npm run build
# RUN cd frontend && npm run build -m development

# Execute
EXPOSE 80
ENV FLASK_APP=app
ENV FLASK_ENV=production
CMD ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "80"]