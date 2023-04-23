pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'sudo apt-get update && sudo apt-get install -y python3-pip' // Install pip
                sh 'pip install pipenv' // Install pipenv
                sh 'pipenv install' // Install dependencies using pipenv
                sh 'pipenv run pip install -r requirements.txt' // Install dependencies from requirements.txt
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
                sh 'pipenv run python manage.py test'  // Run functional tests
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
            sh 'pipenv run python manage.py clean_pyc' // Clean up compiled Python files
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
