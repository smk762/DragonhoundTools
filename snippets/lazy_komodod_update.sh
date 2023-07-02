#!/bin/bash

mkdir -p /home/$USER/daemons
cd /home/$USER/daemons
wget https://github.com/KomodoPlatform/komodo/releases/download/v0.8.0/komodo_0.8.0_linux.zip
unzip komodo_0.8.0_linux.zip
rm komodo_0.8.0_linux.zip
sudo ln -sf /home/$USER/daemons/komodod /usr/local/bin/komodod
sudo ln -sf /home/$USER/daemons/komodo-cli /usr/local/bin/komodo-cli

