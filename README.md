# Automated WordPress Deployment on AWS

This project automates the deployment of a WordPress site on AWS using Jenkins, Ansible, Terraform, and a Python script. The setup involves provisioning AWS resources with Terraform, configuring these resources using Ansible, and automating deployment processes through Jenkins.

## Project Components

- **Terraform**: Provisions the underlying AWS infrastructure including EC2 instances, VPC, and IAM roles.
- **Jenkins**: Automates the deployment pipeline, handles job scheduling, and manages environment variables.
- **Ansible**: Configures AWS instances, installs necessary packages, and sets up WordPress.
- **Python Script**: Performs the installation of the LAMP stack and WordPress on the remote server.

## Requirements

- AWS Account with access to EC2, IAM, VPC, and other necessary services.
- Jenkins server with plugins for Ansible, Git, and Stage Pipeline.
- Ansible installed on the Jenkins server or another control machine.
- Python 3.x installed on the target AWS instances.
- Terraform installed for infrastructure provisioning.

## Setup Instructions

1. **Terraform Setup**:
   - Use Terraform to create the required AWS infrastructure. Adjust the Terraform scripts according to specific AWS setup.
   - Ensure the Terraform state is securely managed and not exposed.

2. **Jenkins Configuration**:
   - Install necessary plugins (Ansible plugin, Git plugin, Terraform plugin, Stage Pipeline.

3. **Ansible Playbook**:
   - Use the provided Ansible playbook to configure the AWS environment and deploy WordPress.
   - Update the playbook with specific AWS instance details and custom configurations as necessary.

4. **Running the Jenkins Pipeline**:
   - Trigger the pipeline manually through Jenkins UI or set up a webhook for automatic triggering upon code commits.
   - Input necessary parameters such as DB_PASSWORD and WP_ADMIN_PASSWORD when prompted.

## Usage

Execute the Jenkins job to start the deployment. The job will:
- Provision AWS resources using Terraform.
- Transfer the Python script to the AWS instance.
- Execute the script to install and configure WordPress.

