#!/bin/bash

# Multi-Agent RFP System Setup Script
# This script sets up the development environment for the RFP automation system

set -e  # Exit on any error

echo "🚀 Setting up Multi-Agent RFP Automation System"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python 3.8+ is available
check_python() {
    print_info "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_status "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# Check if Node.js is available
check_node() {
    print_info "Checking Node.js version..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js $NODE_VERSION found"
    else
        print_error "Node.js not found. Please install Node.js 16+"
        exit 1
    fi
}

# Check if Docker is available (optional)
check_docker() {
    print_info "Checking Docker availability..."
    if command -v docker &> /dev/null; then
        print_status "Docker found"
        DOCKER_AVAILABLE=true
    else
        print_warning "Docker not found. You'll need to install PostgreSQL and Redis manually"
        DOCKER_AVAILABLE=false
    fi
}

# Setup Python backend
setup_backend() {
    print_info "Setting up Python backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        $PYTHON_CMD -m venv venv
        print_status "Virtual environment created"
    fi
    
    # Activate virtual environment and install dependencies
    print_info "Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Python dependencies installed"
    
    # Copy environment file
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_status "Environment file created (.env)"
        print_warning "Please update .env with your configuration"
    fi
    
    cd ..
}

# Setup React frontend
setup_frontend() {
    print_info "Setting up React frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    print_info "Installing Node.js dependencies..."
    npm install
    print_status "Node.js dependencies installed"
    
    cd ..
}

# Setup database services
setup_services() {
    if [ "$DOCKER_AVAILABLE" = true ]; then
        print_info "Setting up database services with Docker..."
        
        # Start PostgreSQL and Redis
        docker-compose up -d postgres redis
        
        # Wait for services to be ready
        print_info "Waiting for services to start..."
        sleep 10
        
        # Check if services are running
        if docker-compose ps | grep -q "postgres.*Up"; then
            print_status "PostgreSQL is running"
        else
            print_error "Failed to start PostgreSQL"
            exit 1
        fi
        
        if docker-compose ps | grep -q "redis.*Up"; then
            print_status "Redis is running"
        else
            print_error "Failed to start Redis"
            exit 1
        fi
        
    else
        print_warning "Docker not available. Please install and configure:"
        print_warning "  - PostgreSQL 13+ (port 5432)"
        print_warning "  - Redis 6+ (port 6379)"
        print_warning "  - Create database 'rfp_system' with user 'rfp_user'"
    fi
}

# Initialize database
init_database() {
    if [ "$DOCKER_AVAILABLE" = true ]; then
        print_info "Initializing database..."
        
        cd backend
        source venv/bin/activate
        
        # Run database initialization
        python database/init_db.py
        print_status "Database initialized with sample data"
        
        cd ..
    else
        print_warning "Skipping database initialization. Run manually after setting up PostgreSQL"
    fi
}

# Create startup scripts
create_scripts() {
    print_info "Creating startup scripts..."
    
    # Make run_system.py executable
    chmod +x run_system.py
    
    # Create quick start script
    cat > start_system.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Multi-Agent RFP System..."

# Start services if using Docker
if command -v docker-compose &> /dev/null; then
    echo "📦 Starting database services..."
    docker-compose up -d postgres redis
    sleep 5
fi

# Start the system
python3 run_system.py
EOF
    
    chmod +x start_system.sh
    print_status "Startup scripts created"
}

# Main setup process
main() {
    echo
    print_info "Starting setup process..."
    
    # Check prerequisites
    check_python
    check_node
    check_docker
    
    # Setup components
    setup_backend
    setup_frontend
    setup_services
    init_database
    create_scripts
    
    echo
    print_status "Setup completed successfully! 🎉"
    echo
    print_info "Next steps:"
    echo "  1. Review and update backend/.env configuration"
    echo "  2. Start the system with: ./start_system.sh"
    echo "  3. Access the dashboard at: http://localhost:3000"
    echo "  4. View API docs at: http://localhost:8000/docs"
    echo
    print_info "Optional management interfaces:"
    if [ "$DOCKER_AVAILABLE" = true ]; then
        echo "  • Database Admin: http://localhost:5050"
        echo "  • Redis Commander: http://localhost:8081"
    fi
    echo
    print_info "For detailed documentation, see README.md"
}

# Run main function
main "$@"