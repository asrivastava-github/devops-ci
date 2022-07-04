# devops-ci

## WSDL2

### Installation

- Install minikube
- Install docker
- Install helm


### Runtime setup

Append ~/.bashrc with below lines

    alias k="minikube kubectl --"
    
    alias kubectl="minikube kubectl --"
    
    source <(k completion bash)

Start docker runtime and minikube using docker as container runtime

    sudo dockerd

    minikube start --driver=docker


### Clone repos

CI repo

    https://github.com/asrivastava-github/devops-ci.git

CD repo

    https://github.com/asrivastava-github/devops-cd.git


### Jenkins setup

    kubectl create namespace jenkins

    helm repo add jenkinsci https://charts.jenkins.io

    helm repo update
    
    helm search repo jenkinsci

cd devops-ci

-------------------------------

### Optional

#### Create persistant volume
    kubectl apply -f jenkins-ci/volume/jenkins-volume.yaml
  
  Minikube configured for hostPath sets the permissions on /data to the root account only. Once the volume is created you will need to manually change the permissions to allow the jenkins account to write its data.
      minikube ssh
      folder jenkins-volume will not be available under /data but you need create and make sure you correct the permission, as below
      sudo chown -R 1000:1000 /data/jenkins-volume


#### Create Jenkins service account to operate
    k apply -f jenkins-ci/service-account/jenkins-sa.yaml

outputs

    serviceaccount/jenkins create
    clusterrole.rbac.authorization.k8s.io/jenkins create
    clusterrolebinding.rbac.authorization.k8s.io/jenkins create


#### Define the Jenkins-values

  nodePort: Because we are using minikube we need to use NodePort as service type. Only cloud providers offer load balancers. We define port 32000 as port.

  Storage:


    storageClass:

    storageClass: jenkins-pv

  serviceAccount: the serviceAccount section of the jenkins-values.yaml file should look like this:

    serviceAccount:
      create: false
    # Service account name is autogenerated by default
    name: jenkins
    annotations: {}

#### Install via helm

    chart=jenkinsci/jenkins
    helm install jenkins -n jenkins -f jenkins-ci/jenkins-values.yaml $chart

-------------------------------

#### Install via helm

    helm install jenkins -n jenkins jenkinsci/jenkins

    # Get your 'admin' user password by running
    kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo


    # expose service to 8080
    kubectl --namespace jenkins port-forward svc/jenkins 8080:8080


#### Docker image

    cd app
    docker build . -t <docker-hub-username>/flaskdemo:1.0.0
    docker build . -t asrivastav11/flaskdemo:1.0.0
    docker login
    docker push asrivastav11/flaskdemo:1.0.0
    docker run -d -p <service-ip>:<service-port>:<container-port> <container-name>









