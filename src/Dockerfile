FROM python:3.8-buster

# Install nodejs
RUN apt-get update && apt-get install -y curl
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash && \
    . /root/.bashrc && \
    sleep 1 && \
    nvm install 12.18.2 && \
    ln -s /root/.nvm/versions/node/v12.18.2/bin/node /usr/local/bin/node && \
    ln -s /root/.nvm/versions/node/v12.18.2/bin/npm /usr/local/bin/npm && \
    ln -s /root/.nvm/versions/node/v12.18.2/bin/npx /usr/local/bin/npx

# Install poetry
RUN pip install poetry

# Copy code
WORKDIR /app
COPY . .

# Install python dependencies
RUN poetry install

# Webpack the js
RUN cd frontend && npm install
RUN cd frontend && ./build.js

# Environment
ENV BLE_DATABASES_DIR=/data/databases
ENV BLE_STRUCTURES_DIR=/data/structures
ENV BLE_DEFAULT_STRUCTURES_DIR=/data/structures-default

# Execute
EXPOSE 8080
CMD ["poetry", "run", "./app.py", "server", "--blueleaks-path", "/data/blueleaks"]