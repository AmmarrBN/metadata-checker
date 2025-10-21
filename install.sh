#!/bin/bash

# Created By github.com/AmmarrBN
# Metadata Checker Tool - Installation Script
# Supports: Linux, Termux, and WSL

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect environment
detect_environment() {
    if [ -n "$TERMUX_VERSION" ]; then
        echo "termux"
    elif grep -q Microsoft /proc/version 2>/dev/null; then
        echo "wsl"
    else
        echo "linux"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install package manager packages
install_packages() {
    local env="$1"
    local packages=("$@")

    log_info "Installing system packages..."

    case $env in
        "termux")
            if command_exists pkg; then
                pkg update && pkg upgrade -y
                for pkg in "${packages[@]}"; do
                    if pkg list-installed | grep -q "$pkg"; then
                        log_info "$pkg is already installed"
                    else
                        pkg install -y "$pkg" || log_warning "Failed to install $pkg"
                    fi
                done
            fi
            ;;
        "wsl"|"linux")
            if command_exists apt-get; then
                # Debian/Ubuntu based
                sudo apt-get update
                sudo apt-get install -y software-properties-common
                sudo add-apt-repository -y ppa:ubuntuhandbook1/exiftool
                sudo apt-get update
                for pkg in "${packages[@]}"; do
                    if dpkg -l | grep -q "^ii  $pkg "; then
                        log_info "$pkg is already installed"
                    else
                        sudo apt-get install -y "$pkg" || log_warning "Failed to install $pkg"
                    fi
                done
            elif command_exists yum; then
                # RHEL/CentOS based
                sudo yum update -y
                sudo yum install -y epel-release
                for pkg in "${packages[@]}"; do
                    if rpm -q "$pkg" >/dev/null 2>&1; then
                        log_info "$pkg is already installed"
                    else
                        sudo yum install -y "$pkg" || log_warning "Failed to install $pkg"
                    fi
                done
            elif command_exists dnf; then
                # Fedora
                sudo dnf update -y
                sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
                for pkg in "${packages[@]}"; do
                    if rpm -q "$pkg" >/dev/null 2>&1; then
                        log_info "$pkg is already installed"
                    else
                        sudo dnf install -y "$pkg" || log_warning "Failed to install $pkg"
                    fi
                done
            elif command_exists pacman; then
                # Arch Linux
                sudo pacman -Syu --noconfirm
                for pkg in "${packages[@]}"; do
                    if pacman -Qi "$pkg" >/dev/null 2>&1; then
                        log_info "$pkg is already installed"
                    else
                        sudo pacman -S --noconfirm "$pkg" || log_warning "Failed to install $pkg"
                    fi
                done
            else
                log_error "Unsupported package manager"
                return 1
            fi
            ;;
    esac
}

# Install Python packages
install_python_packages() {
    log_info "Installing Python packages..."

    # Check jika python sudah di install
    if ! command_exists python3 && ! command_exists python; then
        log_error "Python is not installed. Please install Python 3.7 or higher."
        exit 1
    fi

    if command_exists python3; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        PYTHON_CMD="python"
        PIP_CMD="pip"
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    log_info "Detected Python version: $PYTHON_VERSION"

    # Upgrade pip
    log_info "Upgrading pip..."
    $PIP_CMD install --upgrade pip || log_warning "Failed to upgrade pip"


    local packages=("flask" "werkzeug")
    for pkg in "${packages[@]}"; do
        log_info "Installing $pkg..."
        $PIP_CMD install "$pkg" || log_error "Failed to install $pkg"
    done

    log_success "Python packages installed successfully"
}


install_exiftool_from_source() {
    log_info "Installing ExifTool from source..."

    local install_dir="/usr/local/bin"
    if [ "$ENV" = "termux" ]; then
        install_dir="$PREFIX/bin"
    fi

    cd /tmp
    wget https://exiftool.org/Image-ExifTool-12.76.tar.gz
    tar -xzf Image-ExifTool-12.76.tar.gz
    cd Image-ExifTool-12.76
    perl Makefile.PL
    make
    if [ "$ENV" = "termux" ]; then
        make install
    else
        sudo make install
    fi
    cd ..
    rm -rf Image-ExifTool-12.76*

    log_success "ExifTool installed from source"
}

# Verify installations/cek instalasi
verify_installations() {
    log_info "Verifying installations..."

    local tools=("exiftool" "mediainfo" "ffprobe" "file" "strings")
    local python_packages=("flask" "werkzeug")

    for tool in "${tools[@]}"; do
        if command_exists "$tool"; then
            log_success "$tool is installed: $($tool --version 2>/dev/null | head -n1 || echo "version unknown")"
        else
            log_warning "$tool is not installed or not in PATH"
        fi
    done

    for pkg in "${python_packages[@]}"; do
        if $PYTHON_CMD -c "import $pkg" 2>/dev/null; then
            version=$($PYTHON_CMD -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
            log_success "Python package $pkg is installed: $version"
        else
            log_warning "Python package $pkg is not installed"
        fi
    done

    if $PYTHON_CMD -c "import flask, werkzeug" 2>/dev/null; then
        log_success "All Python dependencies are satisfied"
    else
        log_error "Some Python dependencies are missing"
        exit 1
    fi
}

setup_project() {
    log_info "Setting up project structure..."
    mkdir -p templates static uploads
    local required_files=("app.py" "templates/index.html" "static/style.css" "static/script.js")
    local missing_files=()
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_success "All project files are present"
    else
        log_warning "Missing files: ${missing_files[*]}"
        log_info "Please make sure all project files are in place"
    fi
    # Set permissions for uploads directory
    chmod 755 uploads
    log_success "Project structure setup completed"
}

# Display usage information
#show_usage() {
#    echo -e "${BLUE}Metadata Checker Tool - Installation Script${NC}"
#    echo ""
#    echo "Usage: $0 [OPTIONS]"
#    echo ""
#    echo "Options:"
#    echo "  -h, --help          Show this help message"
#    echo "  -v, --verbose       Enable verbose output"
#    echo "  --skip-packages     Skip system package installation"
#    echo "  --skip-python       Skip Python package installation"
#    echo "  --skip-verification Skip installation verification"
#    echo ""
#    echo "Supported environments:"
#    echo "  - Linux (Debian/Ubuntu, RHEL/CentOS, Fedora, Arch)"
#    echo "  - Termux (Android)"
#    echo "  - WSL (Windows Subsystem for Linux)"
#    echo ""
#}

# Main function
main() {
    local SKIP_PACKAGES=false
    local SKIP_PYTHON=false
    local SKIP_VERIFICATION=false
    local VERBOSE=false
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            --skip-packages)
                SKIP_PACKAGES=true
                shift
                ;;
            --skip-python)
                SKIP_PYTHON=true
                shift
                ;;
            --skip-verification)
                SKIP_VERIFICATION=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    if [ "$VERBOSE" = true ]; then
        set -x
    fi
    log_info "Starting Metadata Checker Tool installation..."
    log_info "Detecting environment..."
    ENV=$(detect_environment)
    log_info "Detected environment: $ENV"
    case $ENV in
        "termux")
            SYSTEM_PACKAGES=("python" "ffmpeg" "mediainfo" "imagemagick" "file" "unzip" "binutils" "wget")
            ;;
        "wsl"|"linux")
            SYSTEM_PACKAGES=("python3" "python3-pip" "ffmpeg" "mediainfo" "imagemagick" "file" "unzip" "binutils" "wget" "perl")
            ;;
        *)
            log_error "Unsupported environment: $ENV"
            exit 1
            ;;
    esac
    if [ "$SKIP_PACKAGES" = false ]; then
        install_packages "$ENV" "${SYSTEM_PACKAGES[@]}"
        if ! command_exists exiftool; then
            log_warning "ExifTool not found in repositories, installing from source..."
            install_exiftool_from_source
        fi
    else
        log_info "Skipping system package installation"
    fi
    if [ "$SKIP_PYTHON" = false ]; then
        install_python_packages
    else
        log_info "Skipping Python package installation"
    fi
    if [ "$SKIP_VERIFICATION" = false ]; then
        verify_installations
    else
        log_info "Skipping installation verification"
    fi
    setup_project
    log_success "Installation completed successfully!"
    echo ""
    log_info "To run the application:"
    echo "  python app.py"
    echo ""
    log_info "Or with custom host/port:"
    echo "  python app.py -r 0.0.0.0:8080"
    echo ""
    log_info "Default URL: http://127.0.0.1:8080"
    echo ""
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ "$(id -u)" -ne 0 ] && [ "$TERMUX_VERSION" = "" ]; then
        log_warning "This script may require root privileges for package installation."
        log_info "If prompted, please enter your password."
        echo ""
    fi
    main "$@"
fi
