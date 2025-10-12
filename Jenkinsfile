pipeline {
    agent any
    environment {
        FLASK_ENV = 'development'
    }
    stages {
        stage('Verify Docker Access') {
            steps {
            sh 'docker version'
        }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-api .'
            }
        }
        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5009:5000 --name flask-api-container flask-api'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying Flask API...'
                // Add deployment logic here
            }
        }
    }
    post {
        always {
            sh 'docker rm -f flask-api-container || true'
            sh 'docker rmi flask-api || true'
        }
        success {
            echo '✅ Build and deployment succeeded.'
        }
        failure {
            echo '❌ Build failed. Check logs for details.'
        }
    }
}
