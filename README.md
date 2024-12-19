# azure-web-app-vfs

![Pylint](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/pylint.yml/badge.svg)
![mypy](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/mypy.yml/badge.svg)
![Flake8](https://github.com/WRLC/azure-web-app-vfs/actions/workflows/flake8.yml/badge.svg)

Flask app to browse and download files from Azure services via Kudu VFS API.

## Local Development

The application comes with `docker-compose.yml` and `Dockerfile` that set up the Flask app and its database.

`docker-compose.yml` defines all the environment variables needed to run the app. (See Production Deployment section for required environment variables.)

### Prerequisites

- Python 3.11+
- [Docker](https://docs.docker.com/get-docker/)
- [local-dev-traefik](https://github.com/WRLC/local-dev-traefik) (for networking between containers)
- [aladin-sp-v3](https://github.com/WRLC/aladin-sp-v3) (for user authorization; requires an Institutional Service for azure-web-app-vfs)

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
    docker exec -i -t azure_web_app_vfs /bin/bash
    ```
   
5. Add your SSO username as an admin via the Flask CLI:

    ```bash
   export mariadb+mariadbconnector://user:password@azure_web_app_vfs_db:3306/mydb
   flask add_admin <your-sso-username>
    ```

The app will be available at [https://azure_web_app_vfs.wrlc.localhost](https://azure_web_app_vfs.wrlc.localhost).

## Production Deployment


### Prerequisites

The repository includes files for deployment to an Ubuntu server running Nginx and MariaDB:

* `/etc/nginx/sites-available/azurefiles.conf` - Nginx configuration file
* `/etc/systemd/system/azurefiles.service` - Systemd service file

The application can be adapted to use any Linux stack with a webserver and database.

For the included configuration, however, the following prerequisites are required:

* Ubuntu 20.04+
* Python 3.11+ (including venv)
* [Nginx](https://nginx.org/en/docs/install.html)
* [MariaDB](https://mariadb.org/download/)
* [aladin-sp-v3](https://github.com/WRLC/aladin-sp-v3) running on a production server (for user authorization; requires an Institutional Service for azure-web-app-vfs)


### Setup

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone git@github.com:WRLC/azure-web-app-vfs.git
    cd azure-web-app-vfs
    ```
   
2. Create a virtual environment and install the dependencies:

    ```bash
    python3 -m venv /path/to/venv
    source /path/to/venv/bin/activate
    poetry install
    ```
   
3. Create the database and add a user with the necessary permissions:

    ```bash
    sudo mysql -u root -p -e "CREATE DATABASE <new_database_name>;"
    sudo mysql -u root -p -e "CREATE USER '<new_user>'@'localhost' IDENTIFIED BY '<new_user_password>';"
    sudo mysql -u root -p -e "GRANT ALL PRIVILEGES ON <new_database_name>.* TO '<new_user>'@'localhost';"
    sudo mysql -u root -p -e "FLUSH PRIVILEGES;"
    ```
   
4. Copy the included systemd service file to the systemd directory:

    ```bash
    sudo cp /etc/systemd/system/azurefiles.service /etc/systemd/system/azurefiles.service
    ```
5. Edit the service file to include the correct paths and environment variables (see environment variable info below):
    ```bash
    sudo nano /etc/systemd/system/azurefiles.service
    ```

6. Start the service and enable it to start on boot:

    ```bash
    sudo systemctl start azurefiles
    sudo systemctl enable azurefiles
    ```

7. Copy the included nginx configuration file to the Nginx sites-available directory, add a symlink to sites-enabled, and restart Nginx:

    ```bash
    sudo cp /etc/nginx/sites-available/azurefiles.conf /etc/nginx/sites-available/azurefiles.conf
    ```
   
8. Edit the nginx configuration file to include the correct server name and paths:
   ```bash
    sudo nano /etc/nginx/sites-available/azurefiles.conf
    ```

9. Add a symlink to sites-enabled and restart Nginx:

    ```bash
    sudo ln -s /etc/nginx/sites-available/azurefiles.conf /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    ```
   
10. Add your SSO username as an admin via the Flask CLI:

    ```bash
    export mariadb+mariadbconnector://<new_user>:<new_user_password>@localhost:3306/<new_database_name>
    flask add_admin <your-sso-username>
    ```
    
11. The app will be available at `https://<server_name>`.

### Environment Variables

The following environment variables are required for the application to run:

* `SECRET_KEY` - Flask secret key
* `SHARED_SECRET` - Shared secret
* `SQLALCHEMY_DATABASE_URI` - Database URL
* `SITE_NAME` - Name of the site
* `SITE_URL` - URL of the site (likely the <server_name> in your Nginx configuration)
* `SAML_SP` - URL for the Aladin-SP service provider
* `COOKIE_ISSUING_FILE` - Path to Aladin-SP's cookie issuing file (likely `/login`)
* `LOGOUT_SCRIPT` - Path to Aladin-SP's logout script (likely `/logout`)
* `COOKIE_PREFIX` - Cookie prefix added by Aladin-SP
* `MEMCACHED_SERVER` - Memcached server URL
* `MEMCACHED_PORT` - Memcached server port
* `SERVICE_SLUG` - Service slug for the application used in the Aladin-SP Service; used with `COOKIE_PREFIX` to construct the cookie name

The included docker-compose file sets these environment variables for local development. For production deployment, these variables should be set in the systemd service file.

## Usage

### Adding Files

Initially no resources will be available for file browsing and downloading. An admin user will need to add a resource at `/resource/new` (or by clicking the "Add Resource" button on the home page).

![Add App Credential](addresource.png)

The following fields are required to add a resource:

* `Name` - The Azure resource's name
* `API URL` - The Azure resource's Kudu API URL (the link value for the "Files" option under "Rest API" in the resource's Advanced Tools, probably `https://<resource_name>.scm.azurewebsites.net/api/vfs`)
* `Username` - The FTPS username from the resource's Deployment Center in the Azure portal
* `Password` - The FTPS password from the resource's Deployment Center in the Azure portal

### Downloading Files

To use the application, users must log in with their SSO credentials.

Once logged in, users should see a list of resources. Clicking a resource name will open file browsing for the resource. Clicking a file name will download the file. Clicking a folder name will open that folder.

![Download File](downloadfile.png)