pipeline {
    agent {
        docker {
            image 'python:3.9' // Docker image to use
             args '-v /var/run/docker.sock:/var/run/docker.sock -v $WORKSPACE:$WORKSPACE -u root' // Mount Jenkins workspace as a volume
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
                sh 'pipenv install --skip-lock' // Create and activate virtual environment, install dependencies (skip lock)
                sh 'pipenv install -r requirements.txt' // Install dependencies from requirements.txt
                //sh 'pipenv run pip install xmlrunner==1.7.7' // Install xmlrunner==1.7.7 specifically
            }
        }

        stage('Test') {
            steps {
                sh 'mkdir -p build/reports' // Create the build/reports directory

                 // Run tests and generate XML reports
                sh "pipenv run python -m unittest discover -s $WORKSPACE -p 'test_*.py' -t $WORKSPACE/build/reports"
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
    }

    post {
        always {
            sh 'find . -name "*.pyc" -delete' // Remove compiled Python files
            junit 'build/reports/**/*.xml'
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, disableDeferredWipeout: true, notFailBuild: true, patterns: [[pattern: '.gitignore', type: 'INCLUDE'],  [pattern: '.propsfile', type: 'EXCLUDE']])
        }

        success {
            echo 'Build successful!' // Display success message
        }

        failure {
            echo 'Build failed!' // Display failure message
        }
    }
}
