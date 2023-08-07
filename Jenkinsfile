#!groovy
def PROJECT_NAME = "meetbouten"
def SLACK_CHANNEL = '#meetbouten-deployments'
def PLAYBOOK = 'deploy.yml'
def SLACK_MESSAGE = [
    "title_link": BUILD_URL,
    "fields": [
        ["title": "Project","value": PROJECT_NAME],
        ["title":"Branch", "value": BRANCH_NAME, "short":true],
        ["title":"Build number", "value": BUILD_NUMBER, "short":true]
    ]
]


pipeline {
    agent any

    options {
        timeout(time: 5, unit: 'HOURS')  // Long timeout because we occasionally have large materialized views
    }

    environment {
        SHORT_UUID = sh( script: "uuidgen | cut -d '-' -f1", returnStdout: true).trim()
        COMPOSE_PROJECT_NAME = "${PROJECT_NAME}-${env.SHORT_UUID}"
        VERSION = env.BRANCH_NAME.replace('/', '-').toLowerCase().replace(
            'main', 'latest'
        )
        IS_RELEASE = "${env.BRANCH_NAME ==~ "release/.*"}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'make test'
            }
        }

        stage('Build') {
            steps {
                sh 'make build'
            }
        }

        stage('Push and deploy') {
            when {
                anyOf {
                    branch 'main'
                    buildingTag()
                    environment name: 'IS_RELEASE', value: 'true'
                }
            }
            stages {
                stage('Push') {
                    steps {
                        retry(3) {
                            sh 'make push'
                        }
                    }
                }

                stage('Deploy to acceptance') {
                    when {
                        anyOf {
                            environment name: 'IS_RELEASE', value: 'true'
                            branch 'main'
                        }
                    }
                    steps {
                        sh 'VERSION=acceptance make push'
                        build job: 'Subtask_Openstack_Playbook', parameters: [
                            string(name: 'PLAYBOOK', value: PLAYBOOK),
                            string(name: 'INVENTORY', value: "acceptance"),
                            string(
                                name: 'PLAYBOOKPARAMS',
                                value: "-e 'deployversion=${VERSION} cmdb_id=app_meetbouten'"
                            )
                        ], wait: true
                    }
                }

                stage('Deploy to production') {
                    when { buildingTag() }
                    steps {
                        sh 'VERSION=production make push'
                        build job: 'Subtask_Openstack_Playbook', parameters: [
                            string(name: 'PLAYBOOK', value: PLAYBOOK),
                            string(name: 'INVENTORY', value: "production"),
                            string(
                                name: 'PLAYBOOKPARAMS',
                                value: "-e 'deployversion=${VERSION} cmdb_id=app_meetbouten'"
                            )
                        ], wait: true

                        slackSend(channel: SLACK_CHANNEL, attachments: [SLACK_MESSAGE <<
                            [
                                "color": "#36a64f",
                                "title": "Deploy to production succeeded :rocket:",
                            ]
                        ])
                    }
                }
            }
        }

    }
    post {
        always {
            sh 'make clean'
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, attachments: [SLACK_MESSAGE <<
                [
                    "color": "#D53030",
                    "title": "Build failed :fire:",
                ]
            ])
        }
    }
}
