pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Set Version') {
            steps {
                script {
                    env.VERSION = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
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
                            echo "Building and pushing ${service}..."
                            bat "docker build -t vrindabs/${service}:${env.VERSION} ."
                            bat "docker tag vrindabs/${service}:${env.VERSION} vrindabs/${service}:latest"
                            bat "docker push vrindabs/${service}:${env.VERSION}"
                            bat "docker push vrindabs/${service}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                // Add kubectl apply commands here if you want
            }
        }
    }
}
