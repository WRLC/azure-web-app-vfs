# azure-web-app-vfs

![Pylint](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/pylint.yml/badge.svg)
![mypy](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/mypy.yml/badge.svg)
![Flake8](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/flake8.yml/badge.svg)

Flask app to download files from Azure services via Kudu VFS API.

## Local Development

The application comes with `docker-compose.yml` and `Dockerfile` that set up the Flask app and its database.

`docker-compose.yml` also defines all the environment variables needed to run the app.

### Prerequisites

- Python 3.11+
- [Docker](https://docs.docker.com/get-docker/)
- [local-dev-traefik](https://github.com/WRLC/local-dev-traefik) (for networking between containers)
- [aladin-sp-v3](https://github.com/WRLC/aladin-sp-v3) (for user authorization)

### Setup

1. Start the `local-dev-traefik` and `aladin-sp-v3` containers

2. Clone the repository and navigate to the project directory:

    ```bash
    git clone git@github.com:WRLC/azure-web-app-vfs.git
    cd azure-web-app-vfs
    ```

3. Start the Flask app:

    ```bash
    docker-compose up
    ```
   
4. SSH into the Flask app container:

    ```bash
    docker exec -it azure_web_app_vfs /bin/bash
    ```
   
5. Add your SSO username as an admin via the Flask CLI:

    ```bash
   export mariadb+mariadbconnector://user:password@azure_web_app_vfs_db:3306/mydb
   flask add_admin <your-sso-username>
    ```

The app will be available at [https://azure_web_app_vfs.wrlc.localhost](https://azure_web_app_vfs.wrlc.localhost).

## Production Deployment

