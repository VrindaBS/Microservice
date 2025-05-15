pipeline {
    agent any

    environment {
        VERSION = sh(script: "git rev-parse --short HEAD || date +%Y%m%d%H%M%S", returnStdout: true).trim()
        DOCKER_REPO = "vrindabs"
    }

    stages {
        stage('Build & Push All Services') {
            steps {
                script {
                    def services = ['adservice', 'checkoutservice', 'frontend', 'paymentservice', 'productcatalogservice']

                    for (service in services) {
                        dir(service) {
                            echo "Building ${service}..."
                            sh "docker build -t ${DOCKER_REPO}/${service}:${VERSION} ."
                            sh "docker tag ${DOCKER_REPO}/${service}:${VERSION} ${DOCKER_REPO}/${service}:latest"
                            sh "docker push ${DOCKER_REPO}/${service}:${VERSION}"
                            sh "docker push ${DOCKER_REPO}/${service}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes configurations...'
                sh 'kubectl apply -f k8s-deployments/'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Fetching running services...'
                sh 'kubectl get svc'
            }
        }
    }
}
