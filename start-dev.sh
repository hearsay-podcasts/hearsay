#!/usr/bin/env bash

# Hearsay Development Startup Script for Linux/Mac
# This script starts the PostgreSQL database, backend API, and frontend server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}Starting Hearsay Development Environment...${NC}"

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Start PostgreSQL database using Docker Compose
echo -e "\n${YELLOW}Starting PostgreSQL database...${NC}"
docker compose up -d

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Stopping all processes...${NC}"
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    echo -e "${GREEN}All processes stopped.${NC}"
    exit 0
}

# Register cleanup on script exit (Ctrl+C)
trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "\n${YELLOW}Starting Backend (FastAPI)...${NC}"
BACKEND_DIR="$SCRIPT_DIR/backend"

if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}Error: Backend directory not found at $BACKEND_DIR${NC}"
    exit 1
fi

cd "$BACKEND_DIR"
uv run uvicorn app.main:app --reload &
BACKEND_PID=$!
echo -e "${GREEN}Backend starting on http://localhost:8000${NC}"

# Wait a moment for backend to initialize
sleep 3

# Start Frontend
echo -e "\n${YELLOW}Starting Frontend (SvelteKit)...${NC}"
FRONTEND_DIR="$SCRIPT_DIR/web"

if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}Error: Frontend directory not found at $FRONTEND_DIR${NC}"
    exit 1
fi

cd "$FRONTEND_DIR"
pnpm dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend starting on http://localhost:5173${NC}"

echo -e "\n${CYAN}========================================${NC}"
echo -e "${CYAN}Hearsay Development Environment Started!${NC}"
echo -e "${CYAN}========================================${NC}"
echo -e "${WHITE}Backend API:  http://localhost:8000${NC}"
echo -e "${WHITE}API Docs:     http://localhost:8000/docs${NC}"
echo -e "${WHITE}Frontend:     http://localhost:5173${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"
echo -e "${CYAN}========================================${NC}\n"

# Wait for any process to exit
wait -n
