pipeline {
    agent any

    stages {
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying resources to local Kubernetes (Minikube)...'
                sh 'kubectl apply -f k8s-deployments/'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Getting services from Kubernetes...'
                sh 'kubectl get svc'
            }
        }
    }
}
