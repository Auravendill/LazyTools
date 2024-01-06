sudo apt install wget tar -y
cd ~/Downloads
wget --content-disposition "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64"
tar xjf firefox-*.tar.bz2
sudo mv firefox /opt
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox
sudo wget https://raw.githubusercontent.com/mozilla/sumo-kb/main/install-firefox-linux/firefox.desktop -P /usr/local/share/applications
