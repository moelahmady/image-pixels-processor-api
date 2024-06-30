# Image Processing and API Service

This Python application processes image data from a CSV file, resizes images, stores them in a PostgreSQL database, and provides an API to retrieve and colorize image frames based on depth ranges.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [Local Setup](#local-setup)
  - [Containerized Setup](#containerized-setup)
- [API Usage](#api-usage)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Features

- Convert CSV data to image
- Resize image width from 200 to 150 pixels
- Store resized images in a PostgreSQL database
- API to request image frames based on depth_min and depth_max
- Apply custom color map to generated frames
- Containerized solution using Docker and Docker Compose

## Prerequisites

- Python 3.12+
- PostgreSQL
- Docker and Docker Compose

## Installation and Setup

### Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-processing-api.git
   cd image-processing-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the following:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   PORT=3001
   OUTPUT_DIR=./output
   ```
   Replace `username`, `password`, `dbname`, and other placeholder values with your desired PostgreSQL credentials and settings.

5. Install Postgres locally:
    
   For macOS using Homebrew:
   ```
   brew install postgresql
   brew services start postgresql
   ```     
   For Ubuntu:

   ```
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

   For Windows:

        Download and install PostgreSQL from [the official website](https://www.postgresql.org/download/windows/).

6. Create a new database and user:

    ```
    psql -U postgres
    CREATE DATABASE image_db;
    CREATE USER image_db_user WITH ENCRYPTED PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE image_db TO image_db_user;
    \q
    ```

7. Update the `.env` file with the new database credentials.

8. Run the application:
   ```
   python app.py
   ```

The API should now be accessible at `http://localhost:3001`.

### Containerized Setup

1. Ensure Docker and Docker Compose are installed on your system.

2. Update the `.env` file with the new database credentials. Note that the postgres db host name should be the same as the db service name in the docker-compose file. In our example, the hostname should be "db".

   ```
   DATABASE_URL=postgresql://username:password@db:5432/dbname
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   PORT=3001
   OUTPUT_DIR=/app/output
   ```

3. **Important**: Create the `output` folder locally in the project root directory. This folder will be mounted as a volume in the Docker container.

   ```
   mkdir output
   ```

   Make sure the `OUTPUT_DIR` in the `.env` file matches the path specified in the `docker-compose.yml` file for the `output` volume mount.

4. Build and run the containers:
   ```
   docker-compose up --build
   ```

This will start both the PostgreSQL database and the Python application. The API will be accessible at `http://localhost:3001`.

## API Usage

1. Process and store the image:
   ```
   POST /process_image
   ```
   This endpoint reads the CSV file, processes the image, and stores it in the database.

2. Retrieve and colorize image frames:
   ```
   GET /get_frames?depth_min=<min_depth>&depth_max=<max_depth>
   ```
   Replace `<min_depth>` and `<max_depth>` with the desired depth range.

   Example:
   ```
   http://localhost:3001/get_frames?depth_min=100&depth_max=200
   ```
   This will return paths to the original and colorized image frames for depths between 100 and 200.

   **Note**: When running the application in a containerized environment, the `/get_frames` API will return the locations of the generated images relative to the container's filesystem. Based on the `docker-compose.yml` configuration, the `/app/output` directory inside the container is mapped to the `./output` directory on the local machine. Therefore, you can find the generated images in the `./output` folder on your local system.

## Development

To make changes to the application:

1. Modify the Python code as needed.
2. If running locally, restart the application.
3. If running containerized, rebuild and restart the containers:
   ```
   docker-compose down
   docker-compose up --build
   ```

## Troubleshooting

- If you encounter database connection issues, ensure that the `DATABASE_URL` in the `.env` file is correct and that PostgreSQL is running.
- For containerized deployment, make sure ports 3001 and 5433 are not in use by other applications.
- Check the console output for any error messages or logs.

For any other issues, please open an issue in the GitHub repository.