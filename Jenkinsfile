pipeline {
    agent any

    stages {
        stage('Set Version') {
            steps {
                script {
                    // Try to get short git commit hash, else fallback to datetime string
                    def gitHash = bat(script: 'git rev-parse --short HEAD', returnStatus: true) == 0 ? 
                                  bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim() : null
                    if (gitHash) {
                        env.VERSION = gitHash
                    } else {
                        // Windows date format: YYYYMMDDHHMMSS with powershell
                        env.VERSION = bat(script: 'powershell -command "(Get-Date).ToString(\\\'yyyyMMddHHmmss\\\')"', returnStdout: true).trim()
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
                            // Use double backslashes in paths and %VAR% for env vars in bat
                            bat "docker build -t %DOCKER_REPO%\\\\${service}:%VERSION% ."
                            bat "docker tag %DOCKER_REPO%\\\\${service}:%VERSION% %DOCKER_REPO%\\\\${service}:latest"
                            bat "docker push %DOCKER_REPO%\\\\${service}:%VERSION%"
                            bat "docker push %DOCKER_REPO%\\\\${service}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes configurations...'
                // Double backslash for folder path
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
