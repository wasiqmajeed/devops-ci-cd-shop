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

        stage('Build the docker image') {
            steps {
//                sh '/usr/local/bin/docker build -t wasiqmajeed/my-shop:${BUILD_NUMBER} .'
                echo "${BUILD_NUMBER}"
                sh "/usr/local/bin/docker stop online-shop || true"
                sh "/usr/local/bin/docker rm online-shop || true"
//                sh '/usr/local/bin/docker run -d --name online-shop -p 8081:5000 wasiqmajeed/my-shop:${BUILD_NUMBER}'
                sh '/usr/local/bin/docker run -d --name online-shop -p 8081:5000 wasiqmajeed/my-shop:latest'
                sh '/usr/local/bin/docker ps -a'
            }
        }
//        stage('Testing the app') { // Skipping for now as I am not testing this part
//            steps {
//                echo 'Testing..'
////                sh 'python3 tests/*.py'
//                withCredentials([usernamePassword(credentialsId: 'sauce-labs-creds',
//                                                passwordVariable: 'SAUCE_ACCESS_KEY',
//                                                usernameVariable: 'SAUCE_USERNAME')])
//                {
//                sh '''
//                for test in tests/*.py; do
//                    python3 "$test" || exit 1
//                done
//                '''
//                }
//            }
//        }
        stage('Push the image to Docker registry'){
            steps {
                script {
                    // 1. Securely log in using the shell
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                     passwordVariable: 'DOCKER_PASS',
                                                     usernameVariable: 'DOCKER_USER')]) {

                        // We use --password-stdin to avoid printing the password to logs
                        sh "echo '$DOCKER_PASS' | /usr/local/bin/docker login -u '$DOCKER_USER' --password-stdin"
                    }
                echo 'Pushing the image to Docker registry'
//                sh '/usr/local/bin/docker push wasiqmajeed/my-shop:${BUILD_NUMBER}'
                sh '/usr/local/bin/docker push wasiqmajeed/my-shop:latest'
                }
            }
        }
// Deploy the new image on ECS using ECR
//        stage('Deply the app using ECS') {
//            steps {
//                echo 'Starting the deployment to ECS'
//
//            }
//
//        }
//        stage('Update K8s Manifests') {
//            steps {
//                // 1. Clone the manifest repository
//                git branch: 'main',
//                    credentialsId: "${GIT_CRED_ID}",
//                    url: "https://${MANIFEST_REPO}"
//
//                // 2. Update the image tag in the deployment file
//                // This replaces the image line with the new build number
//                sh """
//                    sed 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|g' k8s/deployment.yaml
//                """
//                // sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|g' k8s/deployment.yaml
//                // 3. Commit and push changes back to the manifest repo
//                sh """
//                    git config user.email "jenkins@yourdomain.com"
//                    git config user.name "Jenkins CI"
//                    git add k8s/deployment.yaml
//                    git commit -m "Update image to version ${BUILD_NUMBER}"
//                    git push origin main
//                """
//            }
//        }
    }
}