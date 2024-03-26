# BlueLeaks Explorer Dev Notes

Use the `docker-compose.yaml` file in the root of the project for development.

Build and run the containers with:

```sh
docker-compose up --build
```

If you want to rebuild the frontend in development mode so that the [Vue Devtools](https://devtools.vuejs.org/) browser extension works, when the container is up:

```sh
docker-compose exec -w /app/frontend app ./node_modules/vite/bin/vite.js build -m development
```

## Updating dependencies

```sh
cd src
poetry update
cd frontend
npm upgrade
```