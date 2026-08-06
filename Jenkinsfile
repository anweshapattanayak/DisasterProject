pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out DisasterProject code'
            }
        }


        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh 'pip3 install -r requirements.txt'
            }
        }


        stage('Test') {
            steps {
                echo 'Running tests'

                sh 'pip3 install pytest'

                sh '''
                export PATH=$PATH:/var/lib/jenkins/.local/bin
                pytest test_main.py
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'

                sh 'docker build -t disasterproject-app .'
            }
        }

    }

}
