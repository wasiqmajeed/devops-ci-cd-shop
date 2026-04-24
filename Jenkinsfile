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

        stage('Deploy') {
            steps {
                sh '/usr/local/bin/docker build -t wasiqmajeed/my-shop:${BUILD_NUMBER} .'
                echo "${BUILD_NUMBER}"
                sh "/usr/local/bin/docker stop online-shop || true"
                sh "/usr/local/bin/docker rm online-shop || true"
                sh '/usr/local/bin/docker run -d --name online-shop -p 8081:5000 wasiqmajeed/my-shop:${BUILD_NUMBER}'
                sh '/usr/local/bin/docker ps -a'
            }
        }
        stage('Testing the app') {
            steps {
                echo 'Testing..'
//                sh 'python3 tests/*.py'
                withCredentials([usernamePassword(credentialsId: 'sauce-labs-creds',
                                                passwordVariable: 'SAUCE_ACCESS_KEY',
                                                usernameVariable: 'SAUCE_USERNAME')])
                {
                sh '''
                for test in tests/*.py; do
                    python3 "$test" || exit 1
                done
                '''
                }
            }
        }
    }
}