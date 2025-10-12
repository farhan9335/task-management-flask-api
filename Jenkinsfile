pipeline {
    agent any
    environment {
        FLASK_ENV = 'development'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/farhan9335/task-management-flask-api.git'
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
        success {
            echo '✅ Build and deployment succeeded.'
        }
        failure {
            echo '❌ Build failed. Check logs for details.'
        }
    }
}
