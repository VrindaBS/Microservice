pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'vrindabs'
        DOCKER_CREDENTIALS_ID = 'docker-cred'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Set Version') {
            steps {
                script {
                    def commitHash = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.VERSION = commitHash.replaceAll("\\r", "")
                    echo "🔖 Using version: ${env.VERSION}"
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat """
                            echo 🔐 Logging into Docker Hub...
                            docker logout
                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        """
                    }
                }
            }
        }

        stage('Build & Push All Services') {
            steps {
                script {
                    def services = ['adservice', 'checkoutservice', 'frontend', 'paymentservice', 'productcatalogservice']

                    for (service in services) {
                        dir(service) {
                            echo "📦 Building and pushing ${service}..."
                            bat """
                                set VERSION=${env.VERSION}
                                docker build -t ${DOCKERHUB_USER}/${service}:%VERSION% .
                                docker tag ${DOCKERHUB_USER}/${service}:%VERSION% ${DOCKERHUB_USER}/${service}:latest
                                docker push ${DOCKERHUB_USER}/${service}:%VERSION%
                                docker push ${DOCKERHUB_USER}/${service}:latest
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                // bat "kubectl apply -f k8s/"
            }
        }
    }

    post {
        failure {
            echo "❗️ Build failed. Check logs above."
        }
        success {
            echo "✅ All services built and pushed successfully!"
        }
    }
}
