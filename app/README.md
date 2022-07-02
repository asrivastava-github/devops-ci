

###Gcloud - kubctl

    gcloud config set project knowatov
    gcloud config set compute/zone europe-west2-a
    gcloud auth application-default login
    gcloud container clusters create blogapp
    gcloud container clusters create blogapp --num-nodes 1 --region europe-west2 --node-locations europe-west2-a,europe-west2-b
    gcloud container clusters delete blogapp


    gcloud projects list
    PROJECT_ID              NAME              PROJECT_NUMBER
    knowatov                knowatov          258947550115
    peaceful-garden-226800  My First Project  1083672961986
    
    gcloud auth configure-docker
    The following settings will be added to your Docker config file 
    located at [/Users/avinashsrivastava/.docker/config.json]:
     {
      "credHelpers": {
        "gcr.io": "gcloud", 
        "us.gcr.io": "gcloud", 
        "eu.gcr.io": "gcloud", 
        "asia.gcr.io": "gcloud", 
        "staging-k8s.gcr.io": "gcloud", 
        "marketplace.gcr.io": "gcloud"
      }
    }

    Do you want to continue (Y/n)?  y
    
    Docker configuration file updated.
    gcloud docker -- push eu.gcr.io/knowatov/blogapp

~

    docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    blogapp             latest              e5f37e6e24c2        12 hours ago        77.3MB
    alpine              latest              3f53bb00af94        10 days ago         4.41MB

    docket tag blogpp eu.gcr.io/knowatov/blogapp
        
    docker images
    REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
    eu.gcr.io/knowatov/blogapp   1.0.0               e5f37e6e24c2        12 hours ago        77.3MB
    blogapp                      latest              e5f37e6e24c2        12 hours ago        77.3MB
    alpine                       latest              3f53bb00af94        10 days ago         4.41MB

~

    kubectl get nodes
    NAME                                     STATUS    ROLES     AGE       VERSION
    gke-blogapp-default-pool-96373837-6gf6   Ready     <none>    1h        v1.10.9-gke.5
    gke-blogapp-default-pool-d8c5f1e8-pj41   Ready     <none>    1h        v1.10.9-gke.5
    
~

    gcloud compute ssh gke-blogapp-default-pool-d8c5f1e8-pj41 --zone europe-west2-b
    
~

    gcloud container images delete eu.gcr.io/knowatov/blogapp-frontend:1.0.0
    
    
    kubectl create -f deployment/frontend.yml 
    docker images
    gcloud projects list
    docker tag blogpp-frontend eu.gcr.io/knowatov/blogapp-frontend:1.0.0
    gcloud docker -- push eu.gcr.io/knowatov/blogapp-frontend
    
    
#####Deleting containers and LB:
    kubectl delete -f deployment/frontend.yml 
    deployment.extensions "frontend" deleted
    service "frontend" deleted
    
    kubectl delete -f deployment/blogapp.yml 
    deployment.apps "blogapp" deleted
    service "blogapp" deleted


###Removing docker old 

Get the name of user running docker.

    docker ps -a
    docker rm reverent_dewdney
    doceker rm peaceful_leakey
    docker rmi blogapp:latest
    docker images
    docker ps -as
    docker image prune
    docker images

###Remove all <none> images

    docker rmi $(docker images -f "dangling=true" -q)


    Ref: https://stackoverflow.com/questions/33907835/docker-error-cannot-delete-docker-container-conflict-unable-to-remove-reposito 

###Deploy with credential:

    kubectl create secret docker-registry ******* --docker-server=https://eu.gcr.io/ --docker-username=******** --docker-password=************ --docker-email=******@*****.com
    kubectl get secret ****** --output=yaml 
    kubectl create -f deployment/blogapp.yml 
    kubectl get nodes
    kubectl get pods

~

    WARNING: Starting in 1.12, new clusters will have basic authentication disabled by default. Basic authentication can be enabled (or disabled) manually using the `--[no-]enable-basic-auth` flag.
    WARNING: Starting in 1.12, new clusters will not have a client certificate issued. You can manually enable (or disable) the issuance of the client certificate using the `--[no-]issue-client-certificate` flag.
    WARNING: Currently VPC-native is not the default mode during cluster creation. In the future, this will become the default mode and can be disabled using `--no-enable-ip-alias` flag. Use `--[no-]enable-ip-alias` flag to suppress this warning.
    WARNING: Starting in 1.12, default node pools in new clusters will have their legacy Compute Engine instance metadata endpoints disabled by default. To create a cluster with legacy instance metadata endpoints disabled in the default node pool, run `clusters create` with the flag `--metadata disable-legacy-endpoints=true`.
    This will enable the autorepair feature for nodes. Please see https://cloud.google.com/kubernetes-engine/docs/node-auto-repair for more information on node autorepairs.
    WARNING: Starting in Kubernetes v1.10, new clusters will no longer get compute-rw and storage-ro scopes added to what is specified in --scopes (though the latter will remain included in the default --scopes). To use these scopes, add them explicitly to --scopes. To use the new behavior, set container/new_scopes_behavior property (gcloud config set container/new_scopes_behavior true).

~

###Get into Alpine based container

    get the name of container:
    
    docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    2594096d5c62        387da9e422f8        "nginx -g 'daemon of…"   31 minutes ago      Up 31 minutes                           k8s_nginx_frontend-7f66b45bcd-5np9m_default_eb087f75-1917-11e9-8833-025000000001_0
    91c71abc10d1        e5f37e6e24c2        "./interface.py"         32 minutes ago      Up 32 minutes                           k8s_blogapp_blogapp-5f9d8c769-4mqwm_default_ae9f5a15-1917-11e9-8833-025000000001_0
    
    docker exec -it k8s_blogapp_blogapp-5f9d8c769-4mqwm_default_ae9f5a15-1917-11e9-8833-025000000001_0 /bin/ash


###Alipine

    Checking nginx process:
    nginx -t
    
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    
 ~
 
 ###Clean
 
docker image rm eu.gcr.io/knowatov/blogapp-frontend:1.0.0 \
docker build -t eu.gcr.io/knowatov/blogapp-frontend:1.0.0 nginx/ \
kubectl create -f deployment/frontend.yml \
kubectl get pod \

    NAME                        READY     STATUS    RESTARTS   AGE
    blogapp-5f9d8c769-4mqwm     1/1       Running   0          4d
    frontend-7f66b45bcd-sl8pg   1/1       Running   0          1m

kubectl exec -it frontend-7f66b45bcd-sl8pg /bin/bash \

~

    (service)   targetPort == containerPort (deployment)