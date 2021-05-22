sudo pacman -Syu mariadb
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl start mariadb.service
sudo systemctl enable mariadb.service
sudo systemctl status mariadb.service
sudo mysql -u root -p
# GRANT ALL PRIVILEGES ON *.* TO 'username'@'1.2.3.4' WITH GRANT OPTION;
# GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'%' IDENTIFIED BY 'PASSWORD' WITH GRANT OPTION;