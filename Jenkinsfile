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
      passwordVariable: 'GIT_TOKEN'
    )]) {

      sh '''
      rm -rf gitops

      git clone https://github.com/abhigyan-mohanta/k8s-gitops-delivery-platform.git gitops

      cd gitops

      git remote set-url origin https://$GIT_USER:$GIT_TOKEN@github.com/abhigyan-mohanta/k8s-gitops-delivery-platform.git

      cd apps/task-api

      sed -i "s|image:.*|image: $IMAGE:$BUILD_NUMBER|" rollout.yaml

      git config user.email "ci@jenkins"
      git config user.name "jenkins"

      git add .
      git commit -m "update image $BUILD_NUMBER"

      git push origin main
      '''
    }
  }
}
```

}
}
