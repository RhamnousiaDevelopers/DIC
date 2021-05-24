#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import os

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import Debian_iso_creator_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    Debian_iso_creator_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    Debian_iso_creator_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


def update():
    os.system("sudo apt update -y && sudo apt upgrade -y")


def prereq():
    os.system("sudo apt install debootstrap squashfs-tools xorriso isolinux syslinux-efi grub-pc-bin grub-efi-amd64-bin mtools")
    os.system("mkdir -p ~/LIVE_BOOT")

def launch_chroot():
    os.system("sudo debootstrap --arch=amd64 --variant=minbase buster ~/LIVE_BOOT/chroot http://ftp.us.debian.org/debian/")
    os.system("clear")
    print("The Debian based OS has been created. ")
    os.system("sudo chroot ~/LIVE_BOOT/chroot")

def prep_fs():
    os.system("sudo mksquashfs ~/LIVE_BOOT/chroot ~/LIVE_BOOT/staging/live/filesystem.squashfs -e boot")
    os.system("sudo cp ~/LIVE_BOOT/chroot/boot/vmlinuz-* ~/LIVE_BOOT/staging/live/vmlinuz && sudo cp ~/LIVE_BOOT/chroot/boot/initrd.img-* ~/LIVE_BOOT/staging/live/initrd")   #copy kernel and initramfs to live directory
    isolinux_cfg = """
        cat <<\'EOF\' >$HOME/LIVE_BOOT/staging/isolinux/isolinux.cfg
UI vesamenu.c32

MENU TITLE Boot Menu
DEFAULT linux
TIMEOUT 600
MENU RESOLUTION 640 480
MENU COLOR border       30;44   #40ffffff #a0000000 std
MENU COLOR title        1;36;44 #9033ccff #a0000000 std
MENU COLOR sel          7;37;40 #e0ffffff #20ffffff all
MENU COLOR unsel        37;44   #50ffffff #a0000000 std
MENU COLOR help         37;40   #c0ffffff #a0000000 std
MENU COLOR timeout_msg  37;40   #80ffffff #00000000 std
MENU COLOR timeout      1;37;40 #c0ffffff #00000000 std
MENU COLOR msg07        37;40   #90ffffff #a0000000 std
MENU COLOR tabmsg       31;40   #30ffffff #00000000 std

LABEL linux
  MENU LABEL RhamnousiaOS [BIOS/ISOLINUX]
  MENU DEFAULT
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd boot=live

LABEL linux
  MENU LABEL RhamnousiaOS [BIOS/ISOLINUX] (nomodeset)
  MENU DEFAULT
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd boot=live nomodeset
EOF"""

    os.system(isolinux_cfg)
    grub_cfg = """
cat <<\'EOF\' >~/LIVE_BOOT/staging/boot/grub/grub.cfg
search --set=root --file /DEBIAN_CUSTOM

set default=\"0\"
set timeout=30

# If X has issues finding screens, experiment with/without nomodeset.

menuentry \"RhamnousiaOS [EFI/GRUB]\" {
    linux ($root)/live/vmlinuz boot=live
    initrd ($root)/live/initrd
}

menuentry \"RhamnousiaOS [EFI/GRUB] (nomodeset)\" {
    linux ($root)/live/vmlinuz boot=live nomodeset
    initrd ($root)/live/initrd
}
EOF"""

    os.system(grub_cfg)
    grub_standalone_cfg = """
cat <<\'EOF\' >$HOME/LIVE_BOOT/tmp/grub-standalone.cfg
search --set=root --file /DEBIAN_CUSTOM
set prefix=($root)/boot/grub/
configfile /boot/grub/grub.cfg
EOF"""

    os.system(grub_standalone_cfg)
    os.system("touch $HOME/LIVE_BOOT/staging/DEBIAN_CUSTOM")

    #copy BIOS/legacy boot required files to workspace
    os.system("cp /usr/lib/ISOLINUX/isolinux.bin \"~/LIVE_BOOT/staging/isolinux/\" && cp /usr/lib/syslinux/modules/bios/* \"~/LIVE_BOOT/staging/isolinux/\"")
    #copy EFI boot files to ws
    os.system("cp -r /usr/lib/grub/x86_64-efi/* \"~/LIVE_BOOT/staging/boot/grub/x86_64-efi/\"")

def gen_efi_img():
    os.system("grub-mkstandalone --format=x86_64-efi --output=~/LIVE_BOOT/tmp/bootx64.efi --locales=\"\" --fonts=\"\" \"boot/grub/grub.cfg=~/LIVE_BOOT/tmp/grub-standalone.cfg\"")

    make_cmd = """
    (cd $HOME/LIVE_BOOT/staging/EFI/boot && \
    dd if=/dev/zero of=efiboot.img bs=1M count=20 && \
    mkfs.vfat efiboot.img && \
    mmd -i efiboot.img efi efi/boot && \
    mcopy -vi efiboot.img $HOME/LIVE_BOOT/tmp/bootx64.efi ::efi/boot/
)"""
    os.system(make_cmd)

def build_iso(iso_name):

    os.system("xorriso -as mkisofs -iso-level 3 -o \"~/LIVE_BOOT/"+str(iso_name)+".iso\" -full-iso9660-filenames -volid \"OS\" -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin -eltorito0boot isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table --eltorito-catalog isolinux/isolinux.cat -eltorito-alt-boot -e /EFI/boot/efiboot.img -no-emul-boot -isohybrid-gpt-basdat -append_partition 2 0xef ~/LIVE_BOOT/staging/EFI/boot/efiboot.img \"~/LIVE_BOOT/staging\"")



class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("600x450+1509+207")
        top.minsize(1, 1)
        top.maxsize(2945, 1050)
        top.resizable(1,  1)
        top.title("DIC.py")
        top.configure(background="#000000")
        top.configure(highlightcolor="black")

        self.Header = tk.Label(top)
        self.Header.place(relx=0.1, rely=0.022, height=51, width=479)
        self.Header.configure(activebackground="#000000")
        self.Header.configure(activeforeground="white")
        self.Header.configure(activeforeground="#11d839")
        self.Header.configure(background="#000000")
        self.Header.configure(font="-family {DejaVu Sans Mono} -size 15 -weight bold")
        self.Header.configure(foreground="#008000")
        self.Header.configure(text='''Rhamnousia Debian OS (.iso) Creator''')

        self.content = tk.Frame(top)
        self.content.place(relx=0.017, rely=0.133, relheight=0.444
                , relwidth=0.958)
        self.content.configure(relief='groove')
        self.content.configure(borderwidth="2")
        self.content.configure(relief="groove")
        self.content.configure(background="#383838")

        self.Label1 = tk.Label(self.content)
        self.Label1.place(relx=0.017, rely=0.025, height=22, width=249)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="#11d839")
        self.Label1.configure(background="#000000")
        self.Label1.configure(font="-family {DejaVu Sans Mono} -size 10")
        self.Label1.configure(foreground="#11d839")
        self.Label1.configure(text='''Press to install prerequisites''')

        self.install_pre_button = tk.Button(self.content, command=prereq)
        self.install_pre_button.place(relx=0.47, rely=0.025, height=23, width=63)

        self.install_pre_button.configure(activebackground="#f9f9f9")
        self.install_pre_button.configure(background="#ffffff")
        self.install_pre_button.configure(borderwidth="2")
        self.install_pre_button.configure(text='''Install''')

        self.Label2 = tk.Label(self.content)
        self.Label2.place(relx=0.017, rely=0.2, height=21, width=189)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="#11d839")
        self.Label2.configure(background="#000000")
        self.Label2.configure(font="-family {DejaVu Sans Mono} -size 10")
        self.Label2.configure(foreground="#11d839")
        self.Label2.configure(text='''Press to launch Chroot''')

        self.launch_button = tk.Button(self.content)
        self.launch_button.place(relx=0.365, rely=0.2, height=23, width=113)
        self.launch_button.configure(activebackground="#f9f9f9")
        self.launch_button.configure(borderwidth="2")
        self.launch_button.configure(text='''Launch Chroot''', command=launch_chroot)

        
        self.Label4 = tk.Label(self.content)
        self.Label4.place(relx=0.017, rely=0.7, height=21, width=209)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="#11d839")
        self.Label4.configure(background="#000000")
        self.Label4.configure(font="-family {DejaVu Sans Mono} -size 10")
        self.Label4.configure(foreground="#11d839")
        self.Label4.configure(text='''Enter name of output ISO''')

        iso_name = tk.StringVar()
        self.iso_name = tk.StringVar(self.content)
        self.Entry2 = tk.Entry(self.content, textvariable=self.iso_name)
        self.Entry2.place(relx=0.4, rely=0.7, height=23, relwidth=0.463)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="blue")
        self.Entry2.configure(selectforeground="white")

        self.build_button = tk.Button(self.content)
        self.build_button.place(relx=0.887, rely=0.7, height=23, width=53)
        self.build_button.configure(activebackground="#f9f9f9")
        self.build_button.configure(background="#ffffff")
        self.build_button.configure(borderwidth="2")
        self.build_button.configure(text='''build''', command=lambda: build_iso(iso_name))

        self.Label3 = tk.Label(self.content)
        self.Label3.place(relx=0.017, rely=0.35, height=21, width=279)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="#11d839")
        self.Label3.configure(background="#000000")
        self.Label3.configure(font="-family {DejaVu Sans Mono} -size 10")
        self.Label3.configure(foreground="#11d839")
        self.Label3.configure(text='''Now edit the chroot enviroment.''')

        self.prepare_button = tk.Button(self.content)
        self.prepare_button.place(relx=0.017, rely=0.5, height=23, width=153)
        self.prepare_button.configure(activebackground="#f9f9f9")
        self.prepare_button.configure(borderwidth="2")
        self.prepare_button.configure(text='''Prepare Filesystem''', command=prep_fs)

        self.makeefi_button = tk.Button(self.content)
        self.makeefi_button.place(relx=0.313, rely=0.5, height=23, width=163)
        self.makeefi_button.configure(activebackground="#f9f9f9")
        self.makeefi_button.configure(borderwidth="2")
        self.makeefi_button.configure(text='''Generate bootable EFI''', command=gen_efi_img)

if __name__ == '__main__':
    vp_start_gui()





