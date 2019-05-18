pipeline {
  agent none
  environment {
    CODECOV_TOKEN = credentials('codecov-token-system-query')
  }
  stages { stage('Test') { parallel {
    stage('GTX 980 Ti') {
      agent { label 'x86_64 && gpu && nvida-gtx-980ti' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('GTX 1080 Ti') {
      agent { label 'x86_64 && gpu && nvidia-gtx-1080ti' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('RTX 2080 Ti') {
      agent { label 'x86_64 && gpu && nvidia-rtx-2080ti' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Tesla K20Xm') {
      agent { label 'x86_64 && gpu && nvidia-tesla-k20xm' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Tesla K40c') {
      agent { label 'x86_64 && gpu && nvidia-tesla-k40c' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Tesla P100') {
      agent { label 'x86_64 && gpu && nvidia-tesla-p100' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Xeon Phi 7210F') {
      agent { label 'x86_64 && phi && intel-xeon-phi-7210f' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Xeon Phi 7295') {
      agent { label 'x86_64 && phi && intel-xeon-phi-7295' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
    stage('Arm') {
      agent { label 'arm' }
      steps {
        sh "python3 -m coverage run --branch --source . -m unittest -v"
        sh "codecov --build \"${NODE_NAME} ${BUILD_DISPLAY_NAME}\" --token \"${CODECOV_TOKEN}\""
      }
    }
  } } }
}
