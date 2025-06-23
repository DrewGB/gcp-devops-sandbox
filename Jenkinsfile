pipeline {
  agent any

  environment {
    IMAGE_NAME = "gcp-devops-sandbox"
    TAG = "latest"
  }

  stages {
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME:$TAG .'
      }
    }

    stage('Deploy to Minikube') {
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
      }
    }
  }
}
