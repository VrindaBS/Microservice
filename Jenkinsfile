pipeline {
    agent any

    stages {
        stage('Set Version') {
            steps {
                script {
                    def gitHashStatus = bat(script: 'git rev-parse --short HEAD', returnStatus: true)
                    def gitHash = null
                    if (gitHashStatus == 0) {
                        gitHash = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    }

                    if (gitHash) {
                        env.VERSION = gitHash
                    } else {
                        env.VERSION = bat(
                            script: 'powershell -command "(Get-Date).ToString(\'yyyyMMddHHmmss\')"',
                            returnStdout: true
                        ).trim()
                    }

                    env.DOCKER_REPO = "vrindabs"
                    echo "Using version: ${env.VERSION}"
                }
            }
        }

        stage('Build & Push All Services') {
            steps {
                script {
                    def services = ['adservice', 'checkoutservice', 'frontend', 'paymentservice', 'productcatalogservice']

                    for (service in services) {
                        dir(service) {
                            echo "Building ${service}..."
                            bat "docker build -t %DOCKER_REPO%/${service}:%VERSION% ."
                            bat "docker tag %DOCKER_REPO%/${service}:%VERSION% %DOCKER_REPO%/${service}:latest"
                            bat "docker push %DOCKER_REPO%/${service}:%VERSION%"
                            bat "docker push %DOCKER_REPO%/${service}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes configurations...'
                bat 'kubectl apply -f k8s-deployments\\\\'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Fetching running services...'
                bat 'kubectl get svc'
            }
        }
    }
}
