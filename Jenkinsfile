podTemplate(label: 'docker', namespace: 'jenkins',
    containers: [containerTemplate(image: 'docker', name: 'docker', command: 'cat', ttyEnabled: true)],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
        node('docker') {
            container('docker') {
                sh 'docker --version'
                stage('Check out SCM') {
                    checkout scm
                }
                stage('Docker image build') {
                    sh 'docker build -t portal .'
                }

                withCredentials([file(credentialsId: 'google-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    stage('docker login') {
                        sh 'cat ${GOOGLE_APPLICATION_CREDENTIALS} | docker login -u _json_key --password-stdin https://gcr.io'
                    }
                    stage('Update staging') {
                        sh 'docker tag portal gcr.io/cidc-dfci/portal:staging'
                    }
                    stage('Push to repo') {
                        sh 'docker push gcr.io/cidc-dfci/portal:staging'
                    }

                }
            }
        }
}

