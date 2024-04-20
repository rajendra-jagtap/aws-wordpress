import subprocess
import sys

def run_command(command):
    """ Utility function to run a shell command and handle errors. """
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Command succeeded: {' '.join(command)}\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\n{e.stderr}")
        sys.exit(1)

def install_lamp_stack():
    """ Install Apache, MySQL, PHP on a generic Linux server based on available package manager. """
    # Detect the package manager
    pkg_mgr = "yum"
    if subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
        pkg_mgr = "dnf"
    elif subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
        pkg_mgr = "apt"
    
    # Update system
    run_command(['sudo', pkg_mgr, 'update', '-y'])

    # Install packages
    if pkg_mgr in ['yum', 'dnf']:
        run_command(['sudo', pkg_mgr, 'install', '-y', 'httpd', 'mariadb-server', 'php', 'php-mysqlnd'])
    elif pkg_mgr == 'apt':
        run_command(['sudo', 'apt', 'install', '-y', 'apache2', 'mariadb-server', 'php', 'php-mysql'])

    # Start and enable services
    if pkg_mgr in ['yum', 'dnf']:
        run_command(['sudo', 'systemctl', 'start', 'httpd', 'mariadb'])
        run_command(['sudo', 'systemctl', 'enable', 'httpd', 'mariadb'])
    elif pkg_mgr == 'apt':
        run_command(['sudo', 'systemctl', 'start', 'apache2', 'mysql'])
        run_command(['sudo', 'systemctl', 'enable', 'apache2', 'mysql'])

def create_database():
    """ Create MySQL database and user for WordPress """
    commands = [
        "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;",
        "CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'password';",
        "GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';",
        "FLUSH PRIVILEGES;"
    ]
    for command in commands:
        run_command(['sudo', 'mysql', '-e', command])

def download_install_wordpress():
    """ Download and configure WordPress """
    run_command(['wget', '-P', '/tmp', 'https://wordpress.org/latest.tar.gz'])
    run_command(['tar', '-xzf', '/tmp/latest.tar.gz', '-C', '/var/www/html/'])
    run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/var/www/html/wordpress'])
    run_command(['cp', '/var/www/html/wordpress/wp-config-sample.php', '/var/www/html/wordpress/wp-config.php'])
    run_command(["sed", "-i", "s/database_name_here/wordpress/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/username_here/wpuser/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/password_here/password/", "/var/www/html/wordpress/wp-config.php"])

def main():
    install_lamp_stack()
    create_database()
    download_install_wordpress()

if __name__ == '__main__':
    main()