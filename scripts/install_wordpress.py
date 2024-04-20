import subprocess

def install_lamp_stack():
    """ Install Apache, MySQL, PHP on Ubuntu """
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'install', 'apache2', 'mysql-server', 'php', 'php-mysql', 'libapache2-mod-php', '-y'], check=True)

def create_database():
    """ Create MySQL database and user for WordPress """
    commands = [
        "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;",
        "CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'password';",
        "GRANT ALL ON wordpress.* TO 'wpuser'@'localhost';",
        "FLUSH PRIVILEGES;"
    ]
    for command in commands:
        subprocess.run(['sudo', 'mysql', '-e', command], check=True)

def download_install_wordpress():
    """ Download and configure WordPress """
    subprocess.run(['wget', '-P', '/tmp', 'https://wordpress.org/latest.tar.gz'], check=True)
    subprocess.run(['tar', '-xzf', '/tmp/latest.tar.gz', '-C', '/var/www/html/'], check=True)
    subprocess.run(['sudo', 'chown', '-R', 'www-data:www-data', '/var/www/html/wordpress'], check=True)
    subprocess.run(['cp', '/var/www/html/wordpress/wp-config-sample.php', '/var/www/html/wordpress/wp-config.php'], check=True)
    
    subprocess.run(["sed", "-i", "s/database_name_here/wordpress/", "/var/www/html/wordpress/wp-config.php"], check=True)
    subprocess.run(["sed", "-i", "s/username_here/wpuser/", "/var/www/html/wordpress/wp-config.php"], check=True)
    subprocess.run(["sed", "-i", "s/password_here/password/", "/var/www/html/wordpress/wp-config.php"], check=True)

def main():
    install_lamp_stack()
    create_database()
    download_install_wordpress()

if __name__ == '__main__':
    main()
