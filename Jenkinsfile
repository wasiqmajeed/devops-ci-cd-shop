pipeline {
    agent any

    environment {
        IMAGE_NAME     = "wasiqmajeed/my-shop"
        IMAGE_TAG = "${BUILD_NUMBER}"

        // AWS Configs (Replace with your actual values)
        AWS_ACCOUNT_ID = "343147895179"
        AWS_REGION     = "eu-central-1"
        ECR_REPO_NAME  = "my-shop"
        ECS_CLUSTER    = "my-shop-cluster"
        ECS_SERVICE    = "my-shop-web-service"
        TASK_FAMILY    = "my-shop-task"
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
                sh '/usr/local/bin/docker build -t wasiqmajeed/my-shop:${BUILD_NUMBER} .'
                echo "${BUILD_NUMBER}"
//                sh "/usr/local/bin/docker stop online-shop || true"
//                sh "/usr/local/bin/docker rm online-shop || true"
//                sh '/usr/local/bin/docker run -d --name online-shop -p 8081:5000 wasiqmajeed/my-shop:${BUILD_NUMBER}'
//                sh '/usr/local/bin/docker run -d --name online-shop -p 8081:5000 wasiqmajeed/my-shop:latest'
//                sh '/usr/local/bin/docker ps -a'
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
//                sh '/usr/local/bin/docker push wasiqmajeed/my-shop:latest'
                echo 'Pushed the image to Docker registry'
                }
            }
        }

        stage('Push to AWS ECR') {
            steps {
                echo 'Logging into Amazon ECR and pushing...'
                withCredentials([[ $class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials' ]]) {
                    // Authenticate Docker to AWS ECR
//                    sh "/usr/local/bin/aws ecr get-login-password --region ${AWS_REGION} | /usr/local/bin/docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                    // Tag for ECR and push
//                    sh "/usr/local/bin/docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}"
//                    sh "/usr/local/bin/docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest"
//                    sh "/usr/local/bin/docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}"
//                    sh "/usr/local/bin/docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest"
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                echo 'Starting the deployment to ECS...'
                withCredentials([[ $class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials' ]]) {

                    // 1. Download the current active task definition
                    sh "/usr/local/bin/aws ecs describe-task-definition --task-definition ${TASK_FAMILY} --region ${AWS_REGION} --query taskDefinition > task-def.json"

                    // 2. Update the image URI inside the JSON file to point to the new image tag
                    // (Using a simple Python inline script to modify the JSON cleanly without breaking layout)
                    sh """
                    python3 -c "
import json
with open('task-def.json', 'r') as f:
    data = json.load(f)
print("1.",data)

# Strip out metadata AWS rejects on registration
for key in ['taskDefinitionArn', 'revision', 'status', 'requiresAttributes', 'compatibilities', 'registeredAt', 'registeredBy']:
    data.pop(key, None)

print("2.", data)

# Update the image string
//data['containerDefinitions'][0]['image'] = '${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}'
data['containerDefinitions'][0]['image'] = '${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest'

with open('new-task-def.json', 'w') as f:
    json.load = json.dump(data, f)

print("3.", data)
"
                    """

                    // 3. Register the new Task Definition revision in AWS
                    sh "/usr/local/bin/aws ecs register-task-definition --cli-input-json file://new-task-def.json --region ${AWS_REGION}"

                    // 4. Update the ECS Service to pull down the latest task definition revision
                    sh "/usr/local/bin/aws ecs update-service --cluster ${ECS_CLUSTER} --service ${ECS_SERVICE} --task-definition ${TASK_FAMILY} --force-new-deployment --region ${AWS_REGION}"

                    echo 'Deployment triggered successfully!'
                }
            }
        }

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