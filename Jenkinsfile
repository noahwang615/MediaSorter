pipeline {

    agent {
        label 'python-runner'
    }
    
    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        booleanParam(
            name: 'RUN_DOCKER_TESTS',
            defaultValue: false,
            description: 'Run Docker smoke tests (requires a Docker-capable Jenkins agent)'
        )
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

        stage('Docker Smoke Tests') {
            when {
                expression { return params.RUN_DOCKER_TESTS }
            }
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    docker version
                    make test-docker
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results-docker.xml'
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