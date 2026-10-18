# The Seance (How to run guide, may be updated once challenges are hosted on web)

## Run locally

This project runs in Docker and can be started locally on any device with
Docker Desktop and Docker Compose installed.

### 1. Get the repository

Clone the repository and open a terminal in its root directory:

```bash
git clone <repository-url>
cd The_Seance
```

### 2. Start the challenge

The repository's environment configuration provides the values needed by the
application. Start the container with:

```bash
docker compose up --build -d
```

The first run builds the image and installs the Python dependencies. Later
runs can use the same command to start the challenge and apply any updates.

### 3. Open it in a browser

Go to [http://localhost:8080](http://localhost:8080). Docker maps local port
`8080` to the application's port inside the container.

### View logs

To follow the container output:

```bash
docker compose logs -f ctf
```

Chat activity is also written to `logs/ctf_activity.log`.

### Stop the challenge

When finished testing, stop and remove the running container with:

```bash
docker compose down
```
