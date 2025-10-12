pipeline {
    agent any
    environment {
        FLASK_ENV = 'development'  // Used for build-time and runtime
    }
    stages {
        stage('Verify Docker Access') {
            steps {
                sh 'docker version'
            }
        }
        stage('Build Docker Image') {
            steps {
                // Pass FLASK_ENV as a build argument
                sh "docker build -t flask-api --build-arg FLASK_ENV=${FLASK_ENV} ."
            }
        }
        stage('Run Container') {
            steps {
                // Pass FLASK_ENV as a runtime environment variable
                sh """
                docker run -d \
                  --name flask-api-container \
                  -p 5009:5000 \
                  -e FLASK_ENV=${FLASK_ENV} \
                  flask-api
                """
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
