pipeline {
    agent {
        docker {
            image 'python:3.9' // Docker image to use
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root' 
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
                sh 'apt-get update' 
                sh 'apt-get install -y python3-dev python3-pip' // Install Python and pip
                sh 'pip install --upgrade pip'
                sh 'pip install --upgrade pipenv'
            }
        }

        stage('Build') {
            steps {
                sh 'pipenv install --skip-lock' // Create and activate virtual environment, install dependencies (skip lock)
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
            }
        }

        stage('Test - Unit') {
            steps {
                sh 'pipenv run coverage run manage.py test --tag=unit-test'
                sh 'pipenv run coverage xml -o coverage.xml'
                sh 'pipenv run coverage html -d coverage_html'
                archiveArtifacts 'coverage_html/**'
                sh 'pipenv run coverage report'
                publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: 'coverage_html', reportFiles: 'index.html', reportName: 'Code Coverage Report'])
            }
        }

        stage('Test - Integration') {
            steps {
                sh 'pipenv run python manage.py test --tag=integrationTest'  
            }
        }

        stage('Deploy') {
            steps {
                sh 'pipenv run python manage.py migrate' 
                sh 'nohup pipenv run python manage.py runserver & sleep 5' 
                sh 'pipenv run python manage.py test' 
                script {
                    def processIds = sh(script: "ps aux | grep 'python manage.py runserver' | grep -v grep | awk '{print \$2}'", returnStdout: true).trim()
                    if (processIds) {
                        sh "echo '${processIds}' | xargs -r kill -9"
                    }
                }
            }
        }

        stage('Linting') {
            steps {
                sh 'pipenv run pylint Authentication Core Juniors Recruiters Reports --exit-zero --disable=C,E,R' // Run Pylint with the desired score threshold
            }
        }
        
        stage('Code Complexity') {
            steps {
                sh 'pipenv run radon cc . -s --xml -i > complexity.xml' // Run radon cc and generate XML report
                sh 'pipenv run radon mi . -s -n B' // Check maintainability index with threshold B

                publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: '.', reportFiles: 'complexity.xml', reportName: 'Code Complexity Report'])
            }
        } 
    }

    post {
        always {
            sh 'find . -name "*.pyc" -delete' // Remove compiled Python files
            junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
            cleanWs()    
        }

        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}