# Docker Networks

By default, containers are isolated. They cannot talk to each other unless they are on the same Network. Networks act like virtual "cables" 
connecting your containers, allowing them to communicate securely using their container names as hostnames (this is called DNS resolution).

## How to Create and Use a Custom Bridge Network

- Step 1: Create the network: The default driver is "bridge", which is what you usually want for containers on a single machine.
  ```bash
  docker network create my_app_network
  ```
- Step 2: Connect containers to the network When you start a container, attach it to the network using --network.

  Container A (The Database):

  ```bash
  docker run -d \
  --name db_container \
  --network my_app_network \
  postgres:latest
```
Container B (The Web App):
```bash
docker run -d \
  --name web_container \
  --network my_app_network \
  python:3.9-slim
```
Step 3: Verification (How they talk)Because they are on the same custom network, the web container can now "ping" the database simply by using its name: db_container. You do not need to know the IP address.Bash# Go inside the web container and try to ping the db
docker exec -it web_container ping db_container
Summary of CommandsActionCommandList Volumesdocker volume lsInspect Volumedocker volume inspect <volume_name>Delete Volumedocker volume rm <volume_name>List Networksdocker network lsConnect Running Containerdocker network connect <network> <container>
