# DIC
Debian ISO Creator

Debian ISO Creator (DIC) is a easy to use Debian ISO creator written in Python with a simple to use GUI. The steps to install debian ISO Creator are as follows:

![alt text](https://github.com/RhamnousiaDevelopers/DIC/blob/main/DIC.png?raw=true)

```
#check for git & pip3
git --version
pip3 --version

#if git or pip3 is not installed, install it
sudo apt install -y git
sudo apt install python3-pip

#clone the repository
git clone https://github.com/RhamnousiaDevelopers/DIC
cd DIC

#install requirements
pip3 install -r requirements.txt

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

After you exit the chroot environment, open a new terminal and paste this before continuing to build the filesystem/EFI
```
sudo mkdir -p $HOME/LIVE_BOOT/{staging/{EFI/boot,boot/grub/x86_64-efi,isolinux,live},tmp}
```
Now you can press 'Prepare Filesystem'. Then, 'Generate Bootable EFI'.


