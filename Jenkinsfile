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
        stage('Build and Run in Docker') {
            steps {
                script {
                    docker.image('python:3.11').inside {
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements.txt'
                        sh 'python app.py'
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deploying Flask API...'
                // Add deployment script or Docker push here
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
