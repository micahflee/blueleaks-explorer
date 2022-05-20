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

# Copy code
WORKDIR /app
COPY . .

# Install python dependencies
RUN poetry install

# Webpack the js
RUN cd frontend && npm install
RUN cd frontend && export NODE_OPTIONS=--openssl-legacy-provider && ./build.js

# Environment
ENV BLE_DATABASES_DIR=/data/databases
ENV BLE_STRUCTURES_DIR=/data/structures
ENV BLE_DEFAULT_STRUCTURES_DIR=/data/structures-default

# Execute
EXPOSE 8080
CMD ["poetry", "run", "./app.py", "server", "--blueleaks-path", "/data/blueleaks"]