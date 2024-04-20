import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command succeeded:", ' '.join(command))
    except subprocess.CalledProcessError as e:
        print("Command failed:", e.stderr)
        sys.exit(1)

def install_mysql():
    # Check if dnf or yum is available
    pkg_mgr = "dnf" if subprocess.run(["which", "dnf"], stdout=subprocess.PIPE).returncode == 0 else "yum"
    
    # Install MariaDB
    run_command(['sudo', pkg_mgr, 'install', '-y', 'mariadb'])

    # Start and enable MariaDB service
    run_command(['sudo', 'systemctl', 'start', 'mariadb'])
    run_command(['sudo', 'systemctl', 'enable', 'mariadb'])

def install_httpd_php():
    # Assuming the use of yum or dnf
    pkg_mgr = "dnf" if subprocess.run(["which", "dnf"], stdout=subprocess.PIPE).returncode == 0 else "yum"
    
    # Install Apache and PHP
    run_command(['sudo', pkg_mgr, 'install', '-y', 'httpd', 'php', 'php-mysqlnd'])

    # Start and enable Apache
    run_command(['sudo', 'systemctl', 'start', 'httpd'])
    run_command(['sudo', 'systemctl', 'enable', 'httpd'])

def download_install_wordpress():
    # Download and configure WordPress
    run_command(['wget', '-P', '/tmp', 'https://wordpress.org/latest.tar.gz'])
    run_command(['tar', '-xzf', '/tmp/latest.tar.gz', '-C', '/var/www/html/'])
    run_command(['sudo', 'chown', '-R', 'apache:apache', '/var/www/html/wordpress'])

def main():
    install_mysql()
    install_httpd_php()
    download_install_wordpress()

if __name__ == '__main__':
    main()