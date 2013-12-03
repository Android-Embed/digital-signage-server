# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagrantfile targets the vagrant-lxc provider. It should work on other providers given
# a relatively recent version of Vagrant, but your mileage may vary.

Vagrant.configure("2") do |config|
  config.vm.box = "wheezy64"

  config.vm.network :forwarded_port, guest: 8000, host: 8000, host_ip: '0.0.0.0'
  config.vm.network :forwarded_port, guest: 6379, host: 6379, host_ip: '0.0.0.0'
  config.vm.network :forwarded_port, guest: 8983, host: 8983
  config.vm.provision :shell, :inline => <<END
# Check if we need to perform a weekly upgrade - this also triggers initial provisioning
touch -d '-1 week' /tmp/.limit
if ! grep -q contrib /etc/apt/sources.list; then
   echo "deb http://cdn.debian.net/debian wheezy contrib" | sudo tee -a /etc/apt/sources.list
fi

# install base packages
if [ /tmp/.limit -nt /var/cache/apt/pkgcache.bin ]; then
    apt-get -y update
    echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
    apt-get -y dist-upgrade
    apt-get -y install htop tmux vim rsync python-dev python-setuptools libev-dev 
    apt-get -y install sqlite3 redis-server imagemagick bzip2 ttf-mscorefonts-installer
    sudo fc-cache -f -v
    sudo easy_install virtualenv
fi
rm /tmp/.limit

# Since PhantomJS currently has issues running on Debian 7, this tries
# to fix font rendering the hard way using the Infinality stack
if [ ! -f /etc/fonts/infinality ]; then
    sudo apt-get install -y build-essential devscripts git-core
    sudo apt-get install -y docbook-to-man libx11-dev x11proto-core-dev quilt
    cd /home/vagrant
    git clone https://github.com/chenxiaolong/Debian-Packages.git
    cd Debian-Packages/freetype-infinality/
    ./build.sh
    cd ../fontconfig-infinality/
    ./build.sh
    cd ..
    sudo dpkg -i freetype-infinality/*.deb fontconfig-infinality/*.deb
    cd /etc/fonts/infinality
    sudo ./infctl.sh setstyle osx
fi

# setup virtualenv
if [ ! -f /vagrant/env/bin/activate ]; then
    virtualenv /vagrant/env
    . /vagrant/env/bin/activate
    pip install -U gevent celery[redis] uwsgi pygments bpython
    echo ". /vagrant/env/bin/activate" | tee -a /home/vagrant/.bash_profile
fi

# setup phantomjs
if [ ! -h /opt/phantomjs ]; then
    cd /tmp
    wget --no-check-certificate https://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-x86_64.tar.bz2
    cd /opt
    sudo tar -jxvf /tmp/phantomjs-1.9.2-linux-x86_64.tar.bz2
    sudo ln -s phantomjs-1.9.2-linux-x86_64 phantomjs
    rm /tmp/phantomjs-1.9.2-linux-x86_64.tar.bz2
fi
END
end
