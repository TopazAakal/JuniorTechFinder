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
                // sh 'pip install pipenv'
            }
        }

        stage('Build') {
            steps {
                sh 'pipenv --rm' // Remove virtual environment if it exists
                sh 'pipenv install --skip-lock'         // Create and activate virtual environment, install dependencies (skip lock)
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
                
            }
        }

        stage('Test - Unit') {
            steps {
                    sh 'pipenv run coverage run --source=my_project manage.py test --tag=unit-test'
                    sh 'pipenv run coverage xml -o coverage.xml'
            }
        }

        stage('Test - Integration') {
            steps {
                sh 'pipenv run python manage.py test --tag=integrationTest '  
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
        stage('Code Complexity') {
            steps {
                sh 'pipenv run radon cc -a -s -i venv -o radon_report.html .'
            }
        }
    }


    post {
        always {
            sh 'find . -name "*.pyc" -delete' // Remove compiled Python files
            junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, disableDeferredWipeout: true, notFailBuild: true, patterns: [[pattern: '.gitignore', type: 'INCLUDE'],  [pattern: '.propsfile', type: 'EXCLUDE']])
            
            step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])

            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: '.', reportFiles: 'radon_report.html', reportName: 'Code Complexity Report'])
    
        }

        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}