pipeline {
    agent any

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Debug') {
            steps {
                sh 'whoami'         // See which user Jenkins thinks it is
                sh 'which python3'  // See which Python binary Jenkins is using
            }
        }
        stage('Testing the app') {
            steps {
                echo 'Testing..'
                sh 'pip3 install -r requirements.txt'
                sh 'python3 tests/*.py'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t wasiqmajeed/my-shop:${BUILD_NUMBER} .'
                echo "${BUILD_NUMBER}"
                sh "docker stop my-shop-container || true"
                sh "docker rm my-shop-container || true"
                sh 'docker run -d --name online-shop -p 5000:8080 wasiqmajeed/my-shop:${BUILD_NUMBER}'
                sh 'docker ps -a'
            }
        }
    }
}