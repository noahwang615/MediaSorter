pipeline {

    agent {
        label 'python-runner'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('MediaSort Logic Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    make test-mediasort
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results-mediasort.xml'
                    archiveArtifacts artifacts: 'logs/**/*.log', allowEmptyArchive: true
                }
            }
        }

        stage('Make Proofs Logic Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    make test-makeproofs
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results-makeproofs.xml'
                    archiveArtifacts artifacts: 'logs/**/*.log', allowEmptyArchive: true
                }
            }
        }
    }

    // Clean workspace after all stages have completed
    post {
        always {
            cleanWs()
        }
    }
}