# Docker Volumes

By default, any data you create inside a container is "ephemeral"—if you delete the container, that data is gone forever. Volumes are the solution to this. They allow you to store data outside the container’s filesystem so it persists even if the container is destroyed.
<br>
There are two main ways to mount data:

**Named Volumes:** Managed entirely by Docker. You don't worry about where it lives on your hard drive. Best for databases.

**Bind Mounts:** You link a specific folder on your computer to a folder in the container. Best for live code reloading during development.

### How to Create and Mount a Named Volume
- Step 1: Create the volume You can create a volume explicitly before running a container.
```
docker volume create my_database_data
```
- Step 2: Mount it to a container Use the -v (or --mount) flag when starting your container.

`Syntax: -v source_volume_name:target_directory_inside_container`

```bash
# Example: Running a Postgres database and saving its data to our volume
docker run -d \
  --name my-postgres \
  -v my_database_data:/var/lib/postgresql/data \
  postgres:latest
```

Now, even if you run docker rm -f my-postgres, your data remains safely inside my_database_data.

### How to Use a Bind Mount (Direct File Mapping)
This maps a specific path on your host machine to the container.

```bash
# Example: Mapping a 'src' folder on your desktop to '/app' in the container
docker run -d \
  -v /Users/name/project/src:/app \
  python:3.9
```
