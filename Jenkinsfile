pipeline {
  agent any

  environment {
    IMAGE = "docker.io/abhigyanmohanta/task-api"
  }

  stages {

    stage('Build Image') {
      steps {
        sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
      }
    }

    stage('Push Image') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'dockerhub',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )]) {
            sh '''
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            docker push docker.io/abhigyanmohanta/task-api:1
            '''
        }
    }
}

    stage('Update GitOps Repo') {
      steps {
        sh '''
        rm -rf k8s-gitops-delivery-platform
        git clone https://github.com/abhigyan-mohanta/k8s-gitops-delivery-platform.git
        cd k8s-gitops-delivery-platform/apps/task-api

        sed -i "s|image:.*|image: $IMAGE:$BUILD_NUMBER|" rollout.yaml

        git config user.email "ci@jenkins"
        git config user.name "jenkins"

        git commit -am "update image $BUILD_NUMBER"
        git push
        '''
      }
    }

  }
}

