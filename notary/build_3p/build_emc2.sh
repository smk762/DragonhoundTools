#!/bin/bash
cd ~
git clone https://github.com/emc2foundation/einsteinium
cd einsteinium
git checkout master

#!/bin/bash
berkeleydb () {
    EMC2_ROOT="~/einsteinium"
    EMC2_PREFIX="${EMC2_ROOT}/db4"
    mkdir -p $EMC2_PREFIX
    wget -N 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz'
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef db-4.8.30.NC.tar.gz' | sha256sum -c
    tar -xzvf db-4.8.30.NC.tar.gz
    cd db-4.8.30.NC/build_unix/

    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$EMC2_PREFIX

    make install
    cd $EMC2_ROOT
}

buildEMC2 () {
    git pull
    make clean
    ./autogen.sh
    ./configure LDFLAGS="-L${EMC2_PREFIX}/lib/" CPPFLAGS="-I${EMC2_PREFIX}/include/" --with-gui=no --disable-tests --disable-bench --without-miniupnpc --enable-experimental-asm --enable-static --disable-shared
    make -j$(nproc)
}

cd ~/einsteinium
berkeleydb
buildEMC2
