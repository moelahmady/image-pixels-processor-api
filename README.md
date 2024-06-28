# Image Processing and API Service

This Python application processes image data from a CSV file, resizes images, stores them in a PostgreSQL database, and provides an API to retrieve and colorize image frames based on depth ranges.

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
   ```
   Replace `username`, `password`, `dbname`, and other placeholder values with your desired PostgreSQL credentials and settings.

Install Postgres locally:

    - **For macOS using Homebrew**:

        ```bash
        brew install postgresql
        brew services start postgresql
        ```

    - **For Ubuntu**:

        ```bash
        sudo apt update
        sudo apt install postgresql postgresql-contrib
        sudo systemctl start postgresql
        ```

    - **For Windows**:

        Download and install PostgreSQL from [the official website](https://www.postgresql.org/download/windows/).

5. Create a new database and user:

    ```bash
    psql -U postgres
    CREATE DATABASE image_db;
    CREATE USER image_db_user WITH ENCRYPTED PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE image_db TO image_db_user;
    \q
    ```

6. Update the `.env` file with the new database credentials.

7. Run the application:
   ```
   python app.py
   ```

The API should now be accessible at `http://localhost:3001`.

### Containerized Setup

1. Ensure Docker and Docker Compose are installed on your system.

2. Update the `.env` file with the new database credentials. And note that
the postgres db host name should be as the db service name in docker-compose file.
in our Example the hostname should be is "db"

   ```
   DATABASE_URL=postgresql://username:password@db:5432/dbname
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   PORT=3001
   ```

3. Build and run the containers:
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

   If you want to view the genrated images you can copy them from inside the container to your desired path.

   ```
   docker cp image_pixels_colorize-api:/app/colored_images /your/path
   docker cp image_pixels_colorize-api:/app/original_images /your/path
   ```

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