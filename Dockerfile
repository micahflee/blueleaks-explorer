FROM python:3.10-bullseye

# Install updates in container
RUN DEBIAN_FRONTEND=noninteractive && \
    export DEBIAN_FRONTEND && \
    apt-get update && \
    apt-get upgrade --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install nodejs
RUN apt-get update && apt-get install -y curl
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
COPY src .

# Copy the built-in and the default structures
RUN mkdir -p /var/blueleaks-explorer/structures-builtin
COPY structures/* /var/blueleaks-explorer/structures-builtin
RUN mkdir -p /var/blueleaks-explorer/structures-default
COPY structures-default/* /var/blueleaks-explorer/structures-default

# Install python dependencies
RUN poetry install

# Webpack the js
RUN cd frontend && npm install
RUN cd frontend && export NODE_OPTIONS=--openssl-legacy-provider && ./build.js

# Environment
ENV BLE_BLUELEAKS_PATH=/data/blueleaks
ENV BLE_DATABASES_PATH=/data/databases
ENV BLE_STRUCTURES_PATH=/data/structures

# Execute
EXPOSE 8080
ENV FLASK_APP=app
ENV FLASK_ENV=production
CMD ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "80"]