# Build
docker-compose build

# Start
docker-compose up
docker-compose up -d
docker-compose up --build

# Stop
docker-compose stop
docker-compose down

# Manage
docker-compose ps
docker-compose logs
docker-compose logs -f service-name

# Execute
docker-compose exec service-name bash
docker-compose exec database mysql -u root -p
