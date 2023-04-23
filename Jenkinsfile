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
                sh 'pipenv run python manage.py collectstatic --noinput' // Collect static files
            }
        }

        stage('Test') {
            steps {
                sh 'pipenv run python manage.py test' // Run Django tests
            }
        }

        stage('Deploy') {
            steps {
                sh 'pipenv run python manage.py migrate' // Apply database migrations
                sh 'pipenv run python manage.py runserver & sleep 5' // Start Django server in the background
                sh 'pipenv run python manage.py test' // Run functional tests
                sh 'kill $(ps aux | grep "python manage.py runserver" | awk "{print $2}")' // Stop Django server
            }
        }

        stage('Publish') {
            steps {
                sh 'pipenv run python manage.py collectstatic --noinput' // Collect static files
                sh 'pipenv run python manage.py compress --force' // Compress static files
                sh 'pipenv run python manage.py check --deploy' // Run Django deployment checks
                sh 'pipenv run python manage.py s3_sync' // Sync static files to S3 or other storage
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

