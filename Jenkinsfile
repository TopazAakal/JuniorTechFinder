pipeline {
    agent {
        docker {
            image 'python:3.9' // Specify the Docker image to use
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root' // Add -u root option for elevated permissions // Additional Docker-related configuration
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install pipenv') {
            steps {
                sh 'apt-get update' // Update package lists
                sh 'apt-get install -y python3-dev python3-pip' // Install Python and pip
                sh 'pip install pipenv' // Install pipenv
            }
        }

        stage('Build') {
            steps {
                sh 'pipenv install' // Create and activate virtual environment, install dependencies
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
            }
        }

        stage('Test') {
            steps {
                sh 'pipenv run python manage.py test' // Run Django tests
            }
        }

        stage('Deploy') {
            steps {
                sh 'pipenv run python manage.py migrate' // Use pipenv run instead of pipenv shell
                sh 'nohup pipenv run python manage.py runserver & sleep 5' // Use pipenv run instead of pipenv shell
                sh 'pipenv run python manage.py test' // Use pipenv run instead of pipenv shell
                script {
                    def processIds = sh(script: 'pgrep -f "python manage.py runserver"', returnStdout: true).trim()
                    if (processIds) {
                        sh "pkill -F <(echo '${processIds}')"
                }
            }
        }
    }

    post {
        always {
            sh 'find . -name "*.pyc" -delete' // Remove compiled Python files
            junit 'reports/**/*.xml' // Publish JUnit test reports
        }

        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}
