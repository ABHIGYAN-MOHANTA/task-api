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
        sh 'docker push $IMAGE:$BUILD_NUMBER'
      }
    }

    stage('Update GitOps Repo') {
      steps {
        sh '''
        git clone https://github.com/abhigyan-mohanta/k8s-gitops-delivery-platform.git
        cd k8s-gitops-delivery-platform/apps/task-api

        sed -i "s|image:.*|image: $IMAGE:$BUILD_NUMBER|" deployment.yaml

        git config user.email "ci@jenkins"
        git config user.name "jenkins"

        git commit -am "update image $BUILD_NUMBER"
        git push
        '''
      }
    }

  }
}

