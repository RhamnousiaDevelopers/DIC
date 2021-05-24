# DIC
Debian ISO Creator

Debian ISO Creator (DIC) is a easy to use Debian ISO creator with  simple to use GUI. The steps to install debian ISO Creator are as follows:

![alt text](https://github.com/RhamnousiaDevelopers/DIC/blob/main/DIC.png?raw=true)

```
#check for git & pip3
git --version
pip3 --version

#if git or pip3 is not installed, install it
sudo apt install -y git
sudo apt install python3-pip

#install requirements
pip3 install -r requirements.txt

#clone the repository
git clone https://github.com/RhamnousiaDevelopers/DIC
cd DIC

#start DIC
python3 DIC.py
```

here are some useful installs when you are in the Chroot enviroment.
```
apt update && \
apt install --no-install-recommends \
    linux-image-amd64 \
    live-boot \
    systemd-sysv

apt install --no-install-recommends \
    network-manager net-tools wireless-tools wpagui \
    curl openssh-client \
    blackbox xserver-xorg-core xserver-xorg xinit xterm \
    nano && \
apt clean

```

If you want to customize the default root user password use
```
passwd root
```
