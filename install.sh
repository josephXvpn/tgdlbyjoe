#!/bin/bash

# Function to check and install Java
install_java() {
    if type -p java > /dev/null; then
        echo "Java is already installed."
    else
        echo "Java is not installed. Installing the latest version..."
        # Download the latest version of Java from Oracle
        JAVA_VERSION="20"  # Change this to the latest version if needed
        JAVA_TAR="jdk-${JAVA_VERSION}_linux-x64_bin.tar.gz"
        JAVA_URL="https://download.oracle.com/java/${JAVA_VERSION}/latest/${JAVA_TAR}"

        # Create directory for installation if not exist
        sudo mkdir -p /opt/java

        # Download Java
        wget "${JAVA_URL}" -O /tmp/${JAVA_TAR}

        # Extract and install Java
        sudo tar -xzf /tmp/${JAVA_TAR} -C /opt/java

        # Clean up
        rm /tmp/${JAVA_TAR}

        # Set up environment variables
        sudo update-alternatives --install /usr/bin/java java /opt/java/jdk-${JAVA_VERSION}/bin/java 1
        sudo update-alternatives --install /usr/bin/javac javac /opt/java/jdk-${JAVA_VERSION}/bin/javac 1

        echo "Java has been installed."
    fi
}

# Function to install ImageMagick
install_imagemagick() {
    if dpkg -l | grep -q imagemagick; then
        echo "ImageMagick is already installed."
    else
        echo "Installing ImageMagick..."
        sudo apt update
        sudo apt install -y imagemagick
        echo "ImageMagick has been installed."
    fi
}

# Function to check and install Python3 and pip3
install_python_pip() {
    if type -p python3 > /dev/null; then
        echo "Python3 is already installed."
    else
        echo "Python3 is not installed. Installing Python3..."
        sudo apt update
        sudo apt install -y python3
        echo "Python3 has been installed."
    fi

    if type -p pip3 > /dev/null; then
        echo "pip3 is already installed."
    else
        echo "pip3 is not installed. Installing pip3..."
        sudo apt install -y python3-pip
        echo "pip3 has been installed."
    fi
}

# Execute functions
install_java
echo ""
install_imagemagick
echo ""
install_python_pip
echo ""


