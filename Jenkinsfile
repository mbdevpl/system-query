pipeline {
  agent none
  environment {
    CODECOV_TOKEN = credentials('codecov-token-system-query')
  }
  stages { stage('Test') { parallel {
    stage('Test on roma0') {
      agent { label 'roma0' }
      steps {
        sh "git clean -dfx"
        sh "python3.6 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Test on roma6') {
      agent { label 'roma6' }
      steps {
        sh "git clean -dfx"
        sh "python3.6 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Test on kiev0') {
      agent { label 'kiev0' }
      steps {
        sh "git clean -dfx"
        sh "python3.6 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Test on warsaw') {
      agent { label 'warsaw' }
      steps {
        sh "git clean -dfx"
        sh "python3.6 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
  } } }
}
