#!/bin/bash

# Before using this script, you need to make sure the AtomicDEX-Desktop
# repository has been cloned including the recursive submodules. 

# This script takes an optional parameter to define the branch, otherwise it defaults to dev.

cd ~/GITHUB/KP/atomicDEX-Desktop  # Change this to the path you cloned AtomicDEX into
if [[ ${#1} -ne 0  ]]; then
	echo "checking out ${1} branch"
	git checkout $1
else 
	echo "checking out dev branch"
	git checkout dev
fi;

git pull
rm -rf build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ../ -GNinja
cmake --build . --config Release --target atomicdex-desktop
cd bin/AntaraAtomicDexAppDir/usr/bin
./atomicdex-desktop
