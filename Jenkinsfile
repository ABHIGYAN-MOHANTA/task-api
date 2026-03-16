pipeline {
agent any

environment {
IMAGE = "docker.io/abhigyanmohanta/task-api"
}

stages {

```
stage('Checkout') {
  steps {
    checkout scm
  }
}

stage('Build Image') {
  steps {
    sh '''
    docker build -t $IMAGE:$BUILD_NUMBER .
    '''
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
      docker push $IMAGE:$BUILD_NUMBER
      docker logout
      '''
    }
  }
}

stage('Update GitOps Repo') {
  steps {
    withCredentials([usernamePassword(
      credentialsId: 'github',
      usernameVariable: 'GIT_USER',
      passwordVariable: 'GIT_PASS'
    )]) {

      sh '''
      rm -rf k8s-gitops-delivery-platform

      git clone https://$GIT_USER:$GIT_PASS@github.com/abhigyan-mohanta/k8s-gitops-delivery-platform.git

      cd k8s-gitops-delivery-platform/apps/task-api

      sed -i "s|image:.*|image: $IMAGE:$BUILD_NUMBER|" rollout.yaml

      git config user.email "ci@jenkins"
      git config user.name "jenkins"

      git add .
      git commit -m "update image $BUILD_NUMBER"

      git push
      '''
    }
  }
}
```

}
}
