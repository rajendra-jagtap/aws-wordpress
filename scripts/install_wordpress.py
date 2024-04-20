import subprocess

def run_command(command):
    """ Run shell command with error handling and output logging. """
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Command succeeded: {' '.join(command)}\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\n{e.stderr}")
        sys.exit(1)

def install_mysql():
    """ Install MySQL and secure the installation. """
    run_command(['sudo', 'yum', 'install', '-y', 'mariadb-server'])
    run_command(['sudo', 'systemctl', 'start', 'mariadb'])
    run_command(['sudo', 'systemctl', 'enable', 'mariadb'])
    # Run secure installation (automate inputs as needed)
    secure_mysql = subprocess.Popen(['sudo', 'mysql_secure_installation'], stdin=subprocess.PIPE)
    secure_mysql.communicate(input=b'\nn\ny\ny\ny\ny\n').decode()

def install_wordpress():
    """ Download and configure WordPress """
    run_command(['wget', '-P', '/tmp', 'https://wordpress.org/latest.tar.gz'])
    run_command(['tar', '-xzf', '/tmp/latest.tar.gz', '-C', '/var/www/html/'])
    run_command(['sudo', 'chown', '-R', 'apache:apache', '/var/www/html/wordpress'])
    # Configure wp-config.php with environment-specific settings
    run_command(['cp', '/var/www/html/wordpress/wp-config-sample.php', '/var/www/html/wordpress/wp-config.php'])
    # Set database details in wp-config.php (consider securing passwords)
    run_command(["sed", "-i", "s/database_name_here/wordpress/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/username_here/wpuser/", "/var/www/html/wordpress/wp-config.php"])
    run_command(["sed", "-i", "s/password_here/password/", "/var/www/html/wordpress/wp-config.php"])

def main():
    install_mysql()
    install_wordpress()

if __name__ == '__main__':
    main()