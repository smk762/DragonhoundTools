#!/bin/bash

# Use this if you are getting C mismatch errors in build
# rm -rf ~/.cache/vcpkg ~/.vcpkg

export DEBIAN_FRONTEND=noninteractive

# install QT (could also be pip3 depending of your python installation)
pip install aqtinstall
python3 -m aqt install -O $HOME/Qt 5.15.2 linux desktop -b https://qt-mirror.dannhauer.de/ -m qtcharts qtwidgets debug_info qtwebengine qtwebview

sudo apt-get install build-essential \
                    libgl1-mesa-dev \
                    ninja-build \
                    curl \
                    wget \
                    zstd \
                    software-properties-common \
                    lsb-release \
                    libpulse-dev \
                    libtool \
                    autoconf \
                    unzip \
                    libssl-dev \
                    libxkbcommon-x11-0 \
                    libxcb-icccm4 \
                    libxcb-image0 \
                    libxcb1-dev \
                    libxcb-keysyms1-dev \
                    libxcb-render-util0-dev \
                    libxcb-xinerama0 \
                    libgstreamer-plugins-base1.0-dev \
                    git -y

# get llvm
wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
sudo ./llvm.sh 12

# set clang version
sudo apt-get update
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-12 777
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-12 777

# You should add the following environment variables to your `~/.bashrc` or `~/.zshrc` profiles for persistence

export QT_INSTALL_CMAKE_PATH=${HOME}/Qt/5.15.2/5.15.2/gcc_64/lib/cmake
export QT_ROOT=${HOME}/Qt/5.15.2/5.15.2
export Qt5_DIR=${HOME}/Qt/5.15.2/5.15.2/gcc_64/lib/cmake/Qt5
export PATH=${HOME}/Qt/5.15.2/5.15.2/gcc_64/bin:$PATH
export CXX=clang++-12
export CC=clang-12

# install libwally
git clone https://github.com/KomodoPlatform/libwally-core.git
cd libwally-core
./tools/autogen.sh
./configure --disable-shared
sudo make -j2 install

# clone repo and setup submodules
cd ~
git clone --branch dev https://github.com/KomodoPlatform/atomicDEX-Desktop.git --recursive
cd ~/GITHUB/KP/atomicDEX-Desktop/ci_tools_atomic_dex
sudo ./ci_scripts/linux_script.sh
cd ~/GITHUB/KP/atomicDEX-Desktop/ci_tools_atomic_dex/vcpkg-repo
./bootstrap-vcpkg.sh
