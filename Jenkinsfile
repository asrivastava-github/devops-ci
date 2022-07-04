node {
    def app

    stage('Clone repository') {
    
        checkout scm
    }

    stage('Build image') {
  
    //    app = docker.build("asrivastav11/test")
        sh "docker build . -t asrivastav11/flaskdemo:1.0.2"
    }

    stage('Test image') {
  

        // app.inside {
        //     sh 'echo "Tests passed"'
        // }
        sh 'echo "Tests passed"'
    }

    stage('Push image') {
        
        // docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
        //     app.push("${env.BUILD_NUMBER}")
        // }
        sh 'docker image push docker push asrivastav11/flaskdemo:1.0.2'
    }
    
    // stage('Trigger ManifestUpdate') {
    //             echo "triggering updatemanifestjob"
    //             build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
    //     }
}