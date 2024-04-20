import os
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
    """ Install Apache, MariaDB, and PHP on Amazon Linux """
    run_command(['sudo', 'dnf', 'update', '-y'])

    run_command(['sudo', 'dnf', 'install', '-y', 'httpd', 'mariadb', 'php', 'php-mysqlnd'])

    run_command(['sudo', 'systemctl', 'start', 'httpd', 'mariadb'])
    run_command(['sudo', 'systemctl', 'enable', 'httpd', 'mariadb'])

def create_database():
    """ Create MySQL database and user for WordPress """
    db_password = os.getenv('DB_PASSWORD', 'default_db_password')
    commands = [
        "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;",
        f"CREATE USER 'wpuser'@'localhost' IDENTIFIED BY '{db_password}';",
        "GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';",
        "FLUSH PRIVILEGES;"
    ]
    for command in commands:
        run_command(['sudo', 'mysql', '-e', command])

def download_install_wordpress():
    """ Download and configure WordPress """
    wp_password = os.getenv('WP_ADMIN_PASSWORD', 'default_wp_password')
    run_command(['wget', '-P', '/tmp', 'https://wordpress.org/latest.tar.gz'])
    run_command(['tar', '-xzf', '/tmp/latest.tar.gz', '-C', '/var/www/html/'])
    run_command(['sudo', 'chown', '-R', 'apache:apache', '/var/www/html/wordpress'])
   
    run_command(['cp', '/var/www/html/wordpress/wp-config-sample.php', '/var/www/html/wordpress/wp-config.php'])
    run_command(["sed", "-i", "s/database_name_here/wordpress/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/username_here/wpuser/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/password_here/'" + db_password + "'/", "/var/www/html/wordpress/wp-config.php"])

    setup_script = f"""
    wp core install --path="/var/www/html/wordpress" --url="http://rajendra.xyz" --title="Wordpress Test" \
    --admin_user="admin" --admin_password="{wp_password}" --admin_email="rajendra.jagtap8595@gmail.com"
    """
    run_command(['sudo', 'wp', 'cli', 'install', '--allow-root', '--path=/var/www/html/wordpress', setup_script])

def main():
    install_lamp_stack()
    create_database()
    download_install_wordpress()

if __name__ == '__main__':
    main()
