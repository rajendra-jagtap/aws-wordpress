pipeline {
    agent any

    parameters {
        booleanParam(name: 'autoApprove', defaultValue: false, description: 'Automatically run apply after generating plan?')
        choice(name: 'ACTION', choices: ['apply', 'destroy'], description: 'Select whether to apply or destroy the infrastructure.')
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

        //stage('Apply or Destroy') {
        //    steps {
        //        script {
        //            if (params.ACTION == 'apply') {
        //                sh "terraform apply -input=false tfplan"
        //            } else if (params.ACTION == 'destroy') {
        //                sh "terraform destroy -auto-approve"
        //            }
        //        }
        //    }
        //}

        stage('Apply Terraform') {
            steps {
                sh 'terraform destroy -auto-approve'
                script {
                    env.INSTANCE_IP = sh(script: "terraform output -raw instance_ip", returnStdout: true).trim()
                }
            }
        }

        stage('Configure with Ansible') {
            steps {
                writeFile(file: 'ansible_inventory', text: "[wordpress_servers]\n${env.INSTANCE_IP} ansible_user=ec2-user ansible_ssh_private_key_file=/tmp/singapore-keypair.pem")
                ansiblePlaybook(
                    playbook: 'ansible/execute_python_script.yml',
                    inventory: 'ansible_inventory'
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
