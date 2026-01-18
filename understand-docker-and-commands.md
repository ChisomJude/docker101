# Understanding Docker and Docker Commands

## What is Docker?
Docker is a platform that allows developers to package an application and all its dependencies into a **container**.  
This ensures the application runs the same way on any system.

**Key Idea:**  
> "Build once, run anywhere."

---

## Core Docker Concepts

###  Docker Image
- A **blueprint** for creating containers:
- Read-only
- Built from a `Dockerfile`

Example:

```bash
docker pull nginx
```
### Docker Container

A running instance of an image. it is lightweight and isolated

Example:
```bash
docker run nginx
```

### Dockerfile

A text file with instructions to build an image

Example:

```bash
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]

```
### Handy Docker Commands

```
docker <command> <subcommand> [options]

# Example:
docker container run nginx
       ↑         ↑    ↑
    command  subcommand  image

```

#### CONTAINERS

```bash

# ============================================
# RUNNING CONTAINERS
# ============================================


# Run container in foreground (attached mode)

docker run nginx
 

#Run container in background (detached mode) - common

docker run -d nginx
# Returns container ID: a3f5b8c9d1e2...

# Run with custom name (easier to manage!)
docker run -d --name my-web-server nginx

# Run with port mapping (access from your browser!)
docker run -d -p 8080:80 --name web nginx
# Now visit: http://localhost:8080
# -p HOST_PORT:CONTAINER_PORT

# Run with environment variables
docker run -d -e MYSQL_ROOT_PASSWORD=secret123 mysql

# Run with volume (persistent storage)
docker run -d -v /my/data:/var/lib/mysql mysql
# Your laptop's /my/data folder ← → Container's /var/lib/mysql


# ============================================
# LISTING CONTAINERS
# ============================================

# Show running containers
docker ps

# Show all containers (including stopped)
docker ps -a

# Show latest created container
docker ps -l

# Custom format output
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"


# ============================================
# MANAGING CONTAINERS
# ============================================

# Stop container gracefully (waits 10 seconds)
docker stop my-web-server 
#my-web-server is ur containder name

# Stop immediately
docker kill my-web-server

# Start stopped container
docker start my-web-server

# Restart container
docker restart my-web-server

# Pause container (freeze it)
docker pause my-web-server

# Unpause
docker unpause my-web-server

# Remove container (must be stopped first)
docker rm my-web-server

# Remove running container forcefully
docker rm -f my-web-server

# Remove all stopped containers
docker container prune


# ============================================
# INSPECTING CONTAINERS
# ============================================

# View container logs
docker logs my-web-server

# Follow logs in real-time (like tail -f)
docker logs -f my-web-server

# Last 100 lines
docker logs --tail 100 my-web-server

# See resource usage (CPU, Memory, Network)
docker stats my-web-server

# Detailed container information (JSON format)
docker inspect my-web-server

# Get specific info (IP address example)
docker inspect -f '{{.NetworkSettings.IPAddress}}' my-web-server

# See processes running inside container
docker top my-web-server


# ============================================
# INTERACTING WITH CONTAINERS
# ============================================

# Execute command in running container
docker exec my-web-server ls /usr/share/nginx/html

# Open bash shell in running container
docker exec -it my-web-server bash

# Run as specific user
docker exec -u root my-web-server whoami

# Copy files from container to host
docker cp my-web-server:/var/log/nginx/access.log ./access.log

# Copy files from host to container
docker cp index.html my-web-server:/usr/share/nginx/html/
```

---

###  Docker Images 

#### Understanding Images (The Blueprint Analogy)

Image = Blueprint for a House
Container = Actual House Built from Blueprint

One Blueprint (Image) → Many Houses (Containers)

#### Working with Images

```bash
# Full image name format:
registry/username/repository:tag

Examples:
nginx                          # Official image, latest tag
nginx:1.24                     # Official image, specific version
nginx:alpine                   # Official image, alpine variant
myusername/my-app:v1.0        # Your image on Docker Hub
localhost:5000/my-app:latest  # Private registry
gcr.io/myproject/app:prod     # Google Container Registry
```
>Commands and Examples with Images

```bash
# ============================================
# FINDING IMAGES
# ============================================

# Search Docker Hub for images
docker search nginx

# Search with filters
docker search --filter stars=100 nginx


# ============================================
# PULLING IMAGES
# ============================================

# Download image from Docker Hub
docker pull nginx

# Pull specific version (tag)
docker pull nginx:1.24
docker pull nginx:alpine    # Smaller version
docker pull nginx:latest    # Default if no tag specified

# Pull from different registry
docker pull gcr.io/google-samples/hello-app:1.0


# ============================================
# LISTING IMAGES
# ============================================

# Show all local images
docker images

# Show image IDs only
docker images -q

# Filter images
docker images nginx


# ============================================
# EXAMINING IMAGES
# ============================================

# See image layers and history
docker history nginx

# Detailed image information
docker inspect nginx

# See how image was built
docker inspect nginx | grep -A 10 "Cmd"


# ============================================
# REMOVING IMAGES
# ============================================

# Remove single image
docker rmi nginx:alpine

# Remove image by ID
docker rmi a3f5b8c9d1e2

# Force remove (even if containers exist)
docker rmi -f nginx

# Remove all unused images
docker image prune

# Remove ALL images (be careful!)
docker rmi $(docker images -q)
```

### Building Custom Images & Dockerfile Mastery



#### What is a Dockerfile?
```
Dockerfile = Recipe to Build an Image

Recipe for Cake:
1. Mix flour, sugar, eggs
2. Add vanilla extract
3. Bake at 350°F for 30 min

Dockerfile for App:
1. Start with base OS (FROM)
2. Add your code (COPY)
3. Install dependencies (RUN)
4. Set startup command (CMD)
```

> ***A dockerfile is save as Dockerfile or dockerfile without any extension***

#### Sample Docker file 

```bash
# Start from Python base image
# (This already has Python installed!)
FROM python:3.11-slim

# Set working directory inside container
# Like doing "cd /app" inside the container
WORKDIR /app

# Copy requirements file first
# (Docker caches layers - if requirements don't change, 
#  it won't reinstall packages on rebuild!)
COPY requirements.txt .

# Install Python dependencies
# RUN executes commands during IMAGE BUILD
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# (We do this AFTER installing dependencies for better caching)
COPY app.py .

# Expose port (documentation - doesn't actually open port)
EXPOSE 5000

# Command to run when container starts
# CMD executes when CONTAINER RUNS
CMD ["python", "app.py"]
```

#### Building and running your image

```bash
# Build image (don't forget the dot!)
docker build -t my-python-app .
# -t tags the image with a name
# . means "Dockerfile is in current directory"

# Watch the build process - each line is a "layer"!
# Step 1/7 : FROM python:3.11-slim
# Step 2/7 : WORKDIR /app
# Step 3/7 : COPY requirements.txt .
# ... and so on

# List images to see your creation!
docker images

# Run your custom container
docker run -d -p 5000:5000 --name my-app my-python-app

# Test it!
curl http://localhost:5000
# OR open browser: http://localhost:5000

# View logs to see Flask running
docker logs my-app

# Make changes to app.py, rebuild, and run again
# You'll see Docker reuse cached layers!

```