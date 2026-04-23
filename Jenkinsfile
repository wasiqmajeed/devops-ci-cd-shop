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
                sh '/usr/local/bin/docker build -t wasiqmajeed/my-shop:${BUILD_NUMBER} .'
                echo "${BUILD_NUMBER}"
                sh "/usr/local/bin/docker stop my-shop-container || true"
                sh "/usr/local/bin/docker rm my-shop-container || true"
                sh '/usr/local/bin/docker run -d --name online-shop -p 5000:8080 wasiqmajeed/my-shop:${BUILD_NUMBER}'
                sh '/usr/local/bin/docker ps -a'
            }
        }
    }
}