pipeline {
    agent {
        docker {
            image 'ubuntu:latest' // Use the Ubuntu Docker image provided by Jenkins
            label 'docker-ubuntu' // Assign a label to the agent for easy reference
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install virtualenv') {
            steps {
                sh 'apt-get update' // Update package lists
                sh 'apt-get install -y python3-venv' // Install virtualenv
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m venv venv' // Create a virtual environment
                sh 'source venv/bin/activate' // Activate the virtual environment
                sh 'pip install -r requirements.txt' // Install dependencies from requirements.txt
                sh 'python manage.py collectstatic --noinput' // Collect static files
            }
        }

        stage('Test') {
            steps {
                sh 'source venv/bin/activate' // Activate the virtual environment
                sh 'python manage.py test' // Run Django tests
            }
        }

        stage('Deploy') {
            steps {
                sh 'source venv/bin/activate' // Activate the virtual environment
                sh 'python manage.py migrate' // Apply database migrations
                sh 'python manage.py runserver & sleep 5' // Start Django server in the background
                sh 'python manage.py test' // Run functional tests
                sh 'kill $(ps aux | grep "python manage.py runserver" | awk "{print $2}")' // Stop Django server
            }
        }

        stage('Publish') {
            steps {
                sh 'source venv/bin/activate' // Activate the virtual environment
                sh 'python manage.py collectstatic --noinput' // Collect static files
                sh 'python manage.py compress --force' // Compress static files
                sh 'python manage.py check --deploy' // Run Django deployment checks
                sh 'python manage.py s3_sync' // Sync static files to S3 or other storage
            }
        }
    }

    post {
        always {
            sh 'deactivate' // Deactivate the virtual environment
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
