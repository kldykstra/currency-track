#!/bin/bash
# deploy.sh

# requires .env file loaded with REMOTE_HOST
REMOTE_USER="ubuntu"
REMOTE_DIR="/home/ubuntu/currency-track"

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
fi

# Remove the old images
docker rmi currency-track-upload:latest
docker rmi currency-track-database:latest
docker rmi currency-track-dashboard:latest

# Build the image locally for AMD64
echo "Building Docker images locally..."
docker buildx build --no-cache --platform linux/amd64 -t currency-track-upload:latest ./upload
docker buildx build --no-cache --platform linux/amd64 -t currency-track-database:latest ./database
docker buildx build --no-cache --platform linux/amd64 -t currency-track-dashboard:latest ./dashboard

# Save images
docker save currency-track-upload:latest -o upload.tar
docker save currency-track-database:latest -o database.tar
docker save currency-track-dashboard:latest -o dashboard.tar

echo "Deploying to EC2..."

# Remove remote directory
echo "Removing remote directory..."
ssh -i "$SSH_KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" "rm -rf $REMOTE_DIR"

# Create remote directory
echo "Creating remote directory..."
ssh -i "$SSH_KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_DIR"

# Install Docker and Docker Compose if not present
echo "Checking Docker installation..."
ssh -i "$SSH_KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" "
    if ! command -v docker &> /dev/null; then
        echo 'Installing Docker...'
        sudo apt update
        sudo apt install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker ubuntu
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo 'Installing Docker Compose...'
        sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
"

# Copy compose file and all image tars
echo "Copying files..."
scp -i "$SSH_KEY_PATH" compose.yaml .env upload.tar database.tar dashboard.tar "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

# Load and run on remote
echo "Loading and running application..."
ssh -i "$SSH_KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" "
    cd $REMOTE_DIR
    echo 'y' | docker system prune -a
    echo 'y' | docker volume prune -a
    docker-compose down
    docker load -i upload.tar
    docker load -i database.tar
    docker load -i dashboard.tar
    docker-compose -f compose.yaml up -d
    docker-compose ps
"

# Clean up local tar files
echo "Cleaning up..."
rm upload.tar database.tar dashboard.tar

echo "Deployment complete!"