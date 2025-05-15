pipeline {
    agent any

    stages {
        stage('Set Version') {
            steps {
                script {
                    // Try to get short git commit hash, else fallback to datetime string
                    def gitHashStatus = bat(script: 'git rev-parse --short HEAD', returnStatus: true)
                    def gitHash = null
                    if (gitHashStatus == 0) {
                        gitHash = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    }

                    if (gitHash) {
                        env.VERSION = gitHash
                    } else {
                        // Windows date format: YYYYMMDDHHMMSS with powershell
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
                            // Build image with version tag
                            bat "docker build -t %DOCKER_REPO%\\\\${service}:%VERSION% ."
                            // Tag image as latest
                            bat "docker tag %DOCKER_REPO%\\\\${service}:%VERSION% %DOCKER_REPO%\\\\${service}:latest"
                            // Push both tags
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
                // Apply all manifests inside k8s-deployments folder
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
