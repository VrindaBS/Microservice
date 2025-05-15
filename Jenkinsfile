pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'vrindabs'  // Change if your DockerHub username is different
        // Optional: store credentials in Jenkins and reference them
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds' // Create this credential in Jenkins (username/password)
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
                    env.VERSION = commitHash.replaceAll("\\r", "") // remove carriage return
                    echo "Using version: ${env.VERSION}"
                }
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat """
                            echo Logging into Docker Hub...
                            docker logout
                            echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
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
                            echo "Building and pushing ${service}..."

                            try {
                                bat "docker build -t ${DOCKERHUB_USER}/${service}:${env.VERSION} ."
                                bat "docker tag ${DOCKERHUB_USER}/${service}:${env.VERSION} ${DOCKERHUB_USER}/${service}:latest"
                                bat "docker push ${DOCKERHUB_USER}/${service}:${env.VERSION}"
                                bat "docker push ${DOCKERHUB_USER}/${service}:latest"
                            } catch (err) {
                                echo "❌ Failed for ${service}: ${err}"
                                error("❌ Stopping build due to failure in ${service}")
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                // You can add your kubectl commands here, e.g.:
                // bat "kubectl apply -f k8s/"
            }
        }
    }

    post {
        failure {
            echo "❗️ Build failed. Please check the logs above for more info."
        }
        success {
            echo "✅ All services built and pushed successfully!"
        }
    }
}
