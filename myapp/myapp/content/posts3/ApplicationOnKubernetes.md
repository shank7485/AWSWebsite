title: Application containerization and it's deployment on Kubernetes
date: 3/12/2017
details: A tutorial on creating a simple containerzied API and deploying it on a 2 Node Kubernetes cluster.
post_no: 4

It's a world of microservices. With soo many companies containerizing their apps and scaling
them using Kubernetes, it's hard not to ignore.

To an idea of Kubernetes and to play around with it, I created this tutorial to install and deploy dockerized apps on a kubernetes
cluster.

This tutorial has 3 parts:

* Dockerizing an API

* Deploying a Kubernetes cluster

* Deploying the Dockerized API on the cluster and exposing it.

## **Dockering an API** ##

For the purpose of this tutorial, I created a simple Flask API which return the IP address of the host it is running on

    import socket
    import fcntl
    import struct
    from flask import Flask


    app = Flask(__name__)

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
        return str(ip)

    IP_ADDRESS = get_ip_address('eth0')


    @app.route('/')
    def hello_world():
        data = 'API endpoint hitting IP: ' + IP_ADDRESS
        return 'API is working.' + data + "  "


    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)


**To dockerize the above API, the following steps are followed:**

```mkdir flask_api```

```cd flask_api```

```vi flask_api.py```

**Paste the above code in flask_api.py.**

```vi Dockerfile```

**Paste the following Dockerfile.**

    FROM ubuntu:14.04
    RUN apt-get update -y
    RUN apt-get install -y python-pip python-dev build-essential
    COPY . /app
    WORKDIR /app
    RUN pip install -r requirements.txt
    ENTRYPOINT ["python"]
    CMD ["flask_api.py"]

```sudo docker build -t flask_api .```

```sudo docker tag latest```

```sudo docker images```

**The flask_api docker image should be built and should be listed in the image list. Now to deploy this on Kubernetes, it needs to uploaded to Docker Hub.**

```sudo docker push <Repo-name-on-docker-hub>```

**The image should be present in your repository on Docker hub. This will later be used to deploy on the Kubernetes cluster.**

## **Deploying a Kubernetes cluster** ##

For purposes of tutorial, we make a cluster on 3 nodes IPs 192.168.0.1, 192.168.0.2 and 192.168.0.3.

IP 192.168.0.1 is the master. And IP 192.168.0.2 and 192.168.0.3 is where we run pods on.

Do the following steps on all nodes.

**Get repository and add to apt.**

```curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -```

    cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
    deb http://apt.kubernetes.io/ kubernetes-xenial main
    EOF

**Update apt.**

```sudo apt-get update```

**Install kubernetes components.**

```sudo apt-get install -y docker.io kubelet kubeadm kubectl kubernetes-cni```

**To initialize the cluster, this step needs to be done only on the master node which in my case is 192.168.0.1.**

```kubeadm init```

**This will run for sometime and it will finally say something such as;**

    Kubernetes master initialised successfully!

    You can now join any number of machines by running the following on each node:

    kubeadm join --token=<secret_token> 192.168.0.1

**The above kubeadm join command needs to be run on other nodes which needs to be added to the cluster.**

**On the other nodes, install all kubernetes components, do not run kubeadm init, run the join command to add the node to the above created cluster.**

```kubeadm join --token=<secret_token> 192.168.0.1```

**Now we have a kubernetes cluster with one master node at 192.168.0.1 and 2 other nodes at 192.168.0.2 and 192.168.0.3.**

To confirm if cluster is running, run ```kubectl get nodes``` on master to see other 2 nodes.

## **Deploying the Dockerized API on the cluster and exposing it outside the cluster** ##

Now that we have our Docker image and a running Kubernetes cluster, we can start deploying it.

**On master run**

```kubectl run test-api --image=<NAME FROM DOCKER HUB REPO IMAGE> --replicas=2 --port=5000```

**The above command will deploy our API on the cluster.**

Check the deployment using ```kubectl get deployments``` and ```kubectl get pods```

**Now to expose the API hosts outside the master/other pods, we create a  NodePort Service.**

```kubectl expose deployment/api-test --type="NodePort" --port 5000```

```kubectl get services/api-test```

```kubectl describe services/api-test```

**Locate NodePort port number form above command. This is needed to access from outside.**

**To access the deployed API run a Curl to check if its actually running.**

```curl <kubernetes_master_IP>:<NodePort Port>```

**Run the curl a couple of times to observe that the requests are load balanced to different pods on different hosts.**

## **Based on tutorials from:** ##

[http://containertutorials.com/docker-compose/flask-simple-app.html](http://containertutorials.com/docker-compose/flask-simple-app.html)

[http://linoxide.com/devops/setup-kubernetes-1-4-kubeadm-ubuntu/](http://linoxide.com/devops/setup-kubernetes-1-4-kubeadm-ubuntu/)








