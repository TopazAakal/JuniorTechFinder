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
                sh 'source venv/bin/activate' // Activate the virtual environment
                sh 'python manage.py migrate' // Apply database migrations
                sh 'python manage.py runserver & sleep 5' // Start Django server in the background
                sh 'python manage.py test' // Run functional tests
                script {
                    def pid = sh(script: 'ps aux | grep "python manage.py runserver" | grep -v grep | awk \'{print $2}\'', returnStdout: true).trim()
                    sh "kill $pid" // Stop Django server
                }
            }
        }

        
    post {
        always {
            sh 'pipenv --rm' // Remove pipenv virtual environment
            sh 'python manage.py clean_pyc' // Clean up compiled Python files
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

