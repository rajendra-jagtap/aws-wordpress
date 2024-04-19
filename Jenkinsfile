pipeline {
    agent any

    parameters {
    //    string(name: 'environment', defaultValue: 'default', description: 'Workspace/environment file to use for deployment')
    //    string(name: 'version', defaultValue: '', description: 'Version variable to pass to Terraform')
        booleanParam(name: 'autoApprove', defaultValue: false, description: 'Automatically run apply after generating plan?')
    //}
    //
    //environment {
    //    AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
    //    AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
    //    TF_IN_AUTOMATION      = '1'
    }

    stages {
        stage('Plan') {
            steps {
                //script {
                //    currentBuild.displayName = params.version
                //}
                sh '/tmp/terraform init -input=false'
                //sh 'terraform workspace select ${environment}'
                sh "/tmp/terraform plan -input=false -out tfplan --var-file=environments/terraform.tfvars"
                sh '/tmp/terraform show -no-color tfplan > tfplan.txt'
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
                    input message: "Do you want to apply the plan?",
                        parameters: [text(name: 'Plan', description: 'Please review the plan', defaultValue: plan)]
                }
            }
        }

        stage('Apply') {
            steps {
                sh "/tmp/terraform apply -input=false tfplan"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'tfplan.txt'
        }
    }
}
