#!/bin/bash
cd ~
git clone https://github.com/jl777/chips3
cd chips3
git checkout dev


berkeleydb () {
    CHIPS_ROOT="~/chips3"
    CHIPS_PREFIX="${CHIPS_ROOT}/db4"
    mkdir -p $CHIPS_PREFIX
    wget -N 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz'
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef db-4.8.30.NC.tar.gz' | sha256sum -c
    tar -xzvf db-4.8.30.NC.tar.gz
    cd db-4.8.30.NC/build_unix/

    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$CHIPS_PREFIX

    make install
    cd $CHIPS_ROOT
}

buildCHIPS () {
    git pull
    make clean
    ./autogen.sh
    ./configure LDFLAGS="-L${CHIPS_PREFIX}/lib/" CPPFLAGS="-I${CHIPS_PREFIX}/include/" --with-gui=no --disable-tests --disable-bench --without-miniupnpc --enable-experimental-asm --enable-static --disable-shared
    make -j$(nproc)
}

cd ~/chips3
berkeleydb
buildCHIPS
