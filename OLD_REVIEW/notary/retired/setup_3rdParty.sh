mkdir ~/wrappers

# GINCOIN
echo 'sudo -u third_party /home/third_party/gincoin-core/src/gincoind  "$@" -datadir=/home/third_party/.gincoincore' > ~/wrappers/gincoind
chmod -x ~/wrappers/gincoind
sudo ln -s ~/wrappers/gincoin-cli /usr/local/bin/gincoind -f
echo 'sudo -u third_party /home/third_party/gincoin-core/src/gincoin-cli  "$@"' > ~/wrappers/gincoin-cli
chmod -x ~/wrappers/gincoin-cli
sudo ln -s ~/wrappers/gincoin-cli /usr/local/bin/gincoin-cli -f
mkdir ~/.gincoincore
sudo cp /home/third_party/.gincoincore/gincoin.conf ~/.gincoincore/gincoin.conf


# CHIPS
echo 'sudo -u third_party /home/third_party/chips3/src/chipsd  "$@" -datadir=/home/third_party/.chips' > ~/wrappers/chipsd
chmod -x ~/wrappers/chipsd
sudo ln -s ~/wrappers/chipsd-cli /usr/local/bin/chipsd -f
echo 'sudo -u third_party /home/third_party/chips/src/chips-cli  "$@"' > ~/wrappers/chips-cli
chmod -x ~/wrappers/chips-cli
sudo ln -s ~/wrappers/chips-cli /usr/local/bin/chips-cli -f
mkdir ~/.chips
sudo cp /home/third_party/.chips/chips.conf ~/.chips/chips.conf


# EMC2
echo 'sudo -u third_party /home/third_party/einsteinium/src/einsteiniumd  "$@" -datadir=/home/third_party/.einsteinium' > ~/wrappers/einsteiniumd
chmod -x ~/wrappers/einsteiniumd
sudo ln -s ~/wrappers/einsteiniumd-cli /usr/local/bin/einsteiniumd -f
echo 'sudo -u third_party /home/third_party/einsteinium/src/einsteinium-cli  "$@"' > ~/wrappers/einsteinium-cli
chmod -x ~/wrappers/einsteinium-cli
sudo ln -s ~/wrappers/einsteinium-cli /usr/local/bin/einsteinium-cli -f
mkdir ~/.einsteinium
sudo cp /home/third_party/.einsteinium/einsteinium.conf ~/.einsteinium/einsteinium.conf


# GAMECREDITS
echo 'sudo -u third_party /home/third_party/GameCredits/src/gamecreditsd  "$@" -datadir=/home/third_party/.gamecredits' > ~/wrappers/gamecreditsd
chmod -x ~/wrappers/gamecreditsd
sudo ln -s ~/wrappers/gamecreditsd-cli /usr/local/bin/gamecreditsd -f
echo 'sudo -u third_party /home/third_party/GameCredits/src/gamecredits-cli  "$@"' > ~/wrappers/gamecredits-cli
chmod -x ~/wrappers/gamecredits-cli
sudo ln -s ~/wrappers/gamecredits-cli /usr/local/bin/gamecredits-cli -f
mkdir ~/.gamecredits
sudo cp /home/third_party/.gamecredits/gamecredits.conf ~/.gamecredits/gamecredits.conf


# KOMODO (Third party)
cp ~/.komodo/blocks /home/third_party/.komodo3/blocks -r
cp ~/.komodo/chainstate /home/third_party/.komodo3/chainstate -r
cp ~/komodo /home/third_party/komodo -r
echo 'sudo -u third_party /home/third_party/komodo/src/komodod  "$@" -datadir=/home/third_party/.komodo3' > ~/wrappers/komodo3d
chmod -x ~/wrappers/komodo3d
sudo ln -s ~/wrappers/komodo3d /usr/local/bin/komodod -f
echo 'sudo -u third_party /home/third_party/komodo/src/komodo-cli  "$@"' > ~/wrappers/komodo3-cli
chmod -x ~/wrappers/komodo3-cli
sudo ln -s ~/wrappers/komodo3-cli /usr/local/bin/komodo3-cli -f
mkdir ~/.komodo3
sudo cp /home/third_party/.komodo3/komodo.conf ~/.komodo3/komodo.conf


# Change ownership of third_party files/folders to grant main user access permissions
sudo chown third_party:third_party_coins /home/third_party -R

