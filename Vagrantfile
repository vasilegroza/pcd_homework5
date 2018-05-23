# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo "Installing dependencies ..."
sudo apt-get update
sudo apt-get install -y unzip curl jq dnsutils
sudo timedatectl set-ntp no
sudo apt-get install -y ntp
sudo apt-get install -y ntpdate
sudo apt-get install -y ntpstat
echo "Determining Consul version to install ..."
CHECKPOINT_URL="https://checkpoint-api.hashicorp.com/v1/check"
if [ -z "$CONSUL_DEMO_VERSION" ]; then
    CONSUL_DEMO_VERSION=$(curl -s "${CHECKPOINT_URL}"/consul | jq .current_version | tr -d '"')
fi
echo "Fetching Consul version ${CONSUL_DEMO_VERSION} ..."
cd /tmp/
curl -s https://releases.hashicorp.com/consul/${CONSUL_DEMO_VERSION}/consul_${CONSUL_DEMO_VERSION}_linux_amd64.zip -o consul.zip
echo "Installing Consul version ${CONSUL_DEMO_VERSION} ..."
unzip consul.zip
sudo chmod +x consul
sudo mv consul /usr/bin/consul
sudo mkdir /etc/consul.d
sudo chmod a+w /etc/consul.d
sudo apt-get install -y python-pip python-dev libmysqlclient-dev
sudo curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo python get-pip.py
sudo python3 get-pip.py
sudo python3 -m pip install PyMySQL
SCRIPT

$script_s1 = <<SCRIPT
sudo echo 'export MY_IP=172.20.20.10' >> /home/vagrant/.profile
source /home/vagrant/.profile
sudo /sbin/setcap 'cap_net_bind_service=ep' /usr/bin/python3.5
sudo sed -i '$ a 172.20.20.11 s2' /etc/hosts
sudo sed -i '$ a 172.20.20.12 s3' /etc/hosts
sudo sed -i '$ a 172.20.20.13 s4' /etc/hosts
sudo echo yes | sudo cp /vagrant/ntp.conf /etc/
sudo /etc/init.d/ntp restart
consul agent -data-dir=/tmp/consul -node=agent-one -bind=172.20.20.10 -enable-script-checks=true -config-dir=/etc/consul.d > ./consul_agent.log &
SCRIPT

$script_s2 = <<SCRIPT
sudo echo 'export MY_IP=172.20.20.11' >> /home/vagrant/.profile
source /home/vagrant/.profile
sudo /sbin/setcap 'cap_net_bind_service=ep' /usr/bin/python3.5
sudo sed -i '$ a 172.20.20.10 s1' /etc/hosts
sudo sed -i '$ a 172.20.20.12 s3' /etc/hosts
sudo sed -i '$ a 172.20.20.13 s4' /etc/hosts
sudo echo yes | sudo cp /vagrant/ntp.conf /etc/
sudo /etc/init.d/ntp restart
consul agent -data-dir=/tmp/consul -node=agent-two -bind=172.20.20.11 -enable-script-checks=true -config-dir=/etc/consul.d > ./consul_agent.log &
nohup python3.5 -u /vagrant/server.py proxy -proxy_pass=s3 -proxy_port=80 > /vagrant/s2/server.log 2>&1 &
SCRIPT

$script_s3 = <<SCRIPT
sudo echo 'export MY_IP=172.20.20.12' >> /home/vagrant/.profile
source /home/vagrant/.profile
sudo /sbin/setcap 'cap_net_bind_service=ep' /usr/bin/python3.5
sudo sed -i '$ a 172.20.20.10 s1' /etc/hosts
sudo sed -i '$ a 172.20.20.11 s2' /etc/hosts
sudo sed -i '$ a 172.20.20.13 s4' /etc/hosts
sudo echo yes | sudo cp /vagrant/ntp.conf /etc/
sudo /etc/init.d/ntp restart
consul agent -data-dir=/tmp/consul -node=agent-three -bind=172.20.20.12 -enable-script-checks=true -config-dir=/etc/consul.d > ./consul_agent.log &
nohup python3.5 -u /vagrant/server.py proxy -proxy_pass=s4 -proxy_port=80 > /vagrant/s3/server.log &

SCRIPT

$script_s4 = <<SCRIPT
sudo echo 'export MY_IP=172.20.20.13' >> /home/vagrant/.profile
source /home/vagrant/.profile
sudo echo yes | sudo cp /vagrant/ntp_server.conf /etc/ntp.conf
sudo /etc/init.d/ntp restart
sudo /sbin/setcap 'cap_net_bind_service=ep' /usr/bin/python3.5
sudo sed -i '$ a 172.20.20.10 s1' /etc/hosts
sudo sed -i '$ a 172.20.20.11 s2' /etc/hosts
sudo sed -i '$ a 172.20.20.12 s3' /etc/hosts
sudo apt-get update
sudo echo ${MSQL_ROOT_PASSWORD} > /vagrant/s4/db_pass
sudo echo  "mysql-server mysql-server/root_password password ${MSQL_ROOT_PASSWORD}" | debconf-set-selections
sudo echo "mysql-server mysql-server/root_password_again password ${MSQL_ROOT_PASSWORD}" | debconf-set-selections 
sudo apt-get install -y mysql-server
sudo ufw allow mysql
sudo systemctl start mysql
sudo echo yes | sudo cp /vagrant/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
sudo cat /vagrant/init_db.sql | mysql -u root --password=${MSQL_ROOT_PASSWORD} 
consul agent -data-dir=/tmp/consul -node=agent-four -bind=172.20.20.13 -enable-script-checks=true -config-dir=/etc/consul.d > ./consul_agent.log &
nohup python3 -u /vagrant/server.py final > /vagrant/s4/server.log &

SCRIPT
# Specify a Consul version
CONSUL_DEMO_VERSION = ENV['CONSUL_DEMO_VERSION']

# Specify a custom Vagrant box for the demo
DEMO_BOX_NAME = ENV['DEMO_BOX_NAME'] || "debian/stretch64"

MSQL_ROOT_PASSWORD = "homework5"
# Vagrantfile API/syntax version.
# NB: Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
#   config.vm.box = DEMO_BOX_NAME
  config.vm.box = "bento/ubuntu-16.04" # 16.04 LTS
  config.vm.provision "shell",
                          inline: $script,
                          env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}

  config.vm.define "s1" do |s1|
      s1.vm.provision 'shell',
                    inline: $script_s1
      s1.vm.hostname = "s1"
      s1.vm.network "private_network", ip: "172.20.20.10"
      # s1.vm.network "private_network", :type => 'dhcp', :name => 'vboxnet0', :adapter => 2
      s1.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
          vb.customize ["modifyvm", :id, "--memory", 512]
          vb.customize ["modifyvm", :id, "--name", "s1"]
      end
  end

  config.vm.define "s2" do |s2|
      s2.vm.provision 'shell',
                    inline:$script_s2
      s2.vm.hostname = "s2"
      s2.vm.network "private_network", ip: "172.20.20.11"
      # s2.vm.network "private_network", :type => 'dhcp', :name => 'vboxnet0', :adapter => 2
      s2.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--memory", 512]
        vb.customize ["modifyvm", :id, "--name", "s2"]
      end  
    end
  config.vm.define "s3" do |s3|
      s3.vm.provision 'shell',
                    inline:$script_s3
      s3.vm.hostname = "s3"
      s3.vm.network "private_network", ip: "172.20.20.12"
      # s3.vm.network "private_network", :type => 'dhcp', :name => 'vboxnet0', :adapter => 2
      s3.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--memory", 512]
        vb.customize ["modifyvm", :id, "--name", "s3"]
      end  
  end
  config.vm.define "s4" do |s4|
    s4.vm.provision 'shell',
                  inline:$script_s4,
                  env: {'MSQL_ROOT_PASSWORD' => MSQL_ROOT_PASSWORD}
    s4.vm.hostname = "s4"
    s4.vm.network "private_network", ip: "172.20.20.13"
    # s4.vm.network "private_network", :type => 'dhcp', :name => 'vboxnet0', :adapter => 2
    s4.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--name", "s4"]
    end
  end
end