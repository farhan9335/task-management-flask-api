pipeline {
    agent any

    environment {
        FLASK_ENV = 'development'
        IMAGE_NAME = 'flask-api'
        CLUSTER_NAME = 'flask-cluster'
        K8S_MANIFEST_DIR = 'k8s'
    }

    stages {
        stage('Verify Docker Access') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} --build-arg FLASK_ENV=${FLASK_ENV} ."
            }
        }

        stage('Run Container (Local Test)') {
            steps {
                sh """
                docker run -d \
                  --name ${IMAGE_NAME}-container \
                  -p 5009:5000 \
                  -e FLASK_ENV=${FLASK_ENV} \
                  ${IMAGE_NAME}
                """
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh "/tmp/kind load docker-image ${IMAGE_NAME} --name ${CLUSTER_NAME}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying Flask API to Kubernetes...'
                sh """
                kubectl apply -f ${K8S_MANIFEST_DIR}/deployment.yaml
                kubectl apply -f ${K8S_MANIFEST_DIR}/service.yaml
                kubectl rollout status deployment/flask-api-deployment
                """
            }
        }
    }

    post {
        always {
            sh "docker rm -f ${IMAGE_NAME}-container || true"
            sh "docker rmi ${IMAGE_NAME} || true"
        }
        success {
            echo '✅ Build and deployment to Kubernetes succeeded.'
        }
        failure {
            echo '❌ Build or deployment failed. Check logs for details.'
        }
    }
}
