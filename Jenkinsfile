pipeline {
    agent any

    environment {
        DB_PASSWORD = ''
        WP_ADMIN_PASSWORD = ''
    }

    parameters {
        booleanParam(name: 'autoApprove', defaultValue: false, description: 'Automatically run apply after generating plan?')
        password(name: 'DB_PASSWORD', defaultValue: '', description: 'Database password')
        password(name: 'WP_ADMIN_PASSWORD', defaultValue: '', description: 'WordPress Admin password')
    }

    stages {
        stage('Init') {
            steps {
                sh 'terraform init -input=false -backend-config="bucket=rajendra-terraform" -backend-config="key=wordpress.tfstate" -backend-config="region=ap-south-1"'
            }
        }

        stage('Plan') {
            steps {
                sh "terraform plan -input=false -out=tfplan --var-file=terraform.tfvars"
                sh 'terraform show -no-color tfplan > tfplan.txt'
            }
        }

        stage('Approval') {
            when {
                not {
                    equals expected: true, actual: params.autoApprove
                }
            }

            steps {
                script {
                    def plan = readFile 'tfplan.txt'
                    input message: "Review the plan and choose an action",
                        parameters: [text(name: 'Plan', description: 'Please review the plan:', defaultValue: plan)]
                }
            }
        }

        stage('Apply Terraform') {
            steps {
                sh 'terraform apply -auto-approve'
                script {
                    env.INSTANCE_IP = sh(script: "terraform output -raw instance_ip", returnStdout: true).trim()
                }
            }
        }

        stage('Configure with Ansible') {
            steps {
                writeFile(file: 'ansible_inventory', text: "[wordpress_servers]\n${env.INSTANCE_IP} ansible_user=ec2-user ansible_ssh_private_key_file=/tmp/singapore-keypair.pem")
                def extraVars = [
                    'db_password': "${env.DB_PASSWORD}",
                    'wp_admin_password': "${env.WP_ADMIN_PASSWORD}"
                ]
                def extraVarsString = extraVars.collect { key, value -> "$key='$value'" }.join(' ')
                ansiblePlaybook(
                    playbook: 'ansible/execute_python_script.yml',
                    inventory: 'ansible_inventory',
                    extras: "--extra-vars '${extraVarsString}'"
                    //extras: "--extra-vars '${extraVars.collect{key, value -> "$key=$value"}.join(' ')}'"
                )
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'tfplan.txt'
        }
        success {
            echo "Operation ${params.ACTION} completed successfully!"
        }
        failure {
            echo "Operation ${params.ACTION} failed."
        }
    }
}
