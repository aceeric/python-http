# Python HTTP/S Server DaemonSet

Minimal HTTP/HTTPS server for testing Ingresses, Load Balancers, etc.

## Quick Start

Create a namespace `python-http`, a `DaemonSet`, a `ConfigmMap` with the server Python code, and a `Service`:

`kubectl kustomize | kubectl apply -f -`

## Port forward to the server service

By default, the server serves HTTP on port 80:
```
kubectl -n python-http port-forward svc/python-http 8080:80
```

## Tail the DaemonSet logs
The logs will also print all headers received from the client.
```
kubectl -n python-http logs ds/python-http -f
```

## Send it some traffic
```
while true; do curl -H "X-Frobozz: $RANDOM" http://localhost:8080; sleep 1s; done
```

## Response
```
2022-09-10 22:14:32.361601 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:14:33.374368 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:14:34.404922 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:14:35.437020 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:14:36.468997 -- python-http-np7s2 -- 10.200.127.200
```

## If an Ingress controller is present

If you are running an ingress controller, you can access the service from outside the cluster. The example below was run against a single-node Kubernetes cluster running in a VM provisioned by [Desktop Kubernetes](https://github.com/aceeric/desktop-kubernetes). The single node VM has IP address 192.168.56.200. [Traefik](https://doc.traefik.io/traefik/getting-started/quick-start-with-kubernetes/) was installed as a `NodePort` service on node port 30080 to serve port 80 traffic into the cluster:

```
$ kubectl -n traefik get svc
NAME                        TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
traefik-dashboard-service   NodePort   10.32.0.218   <none>        8080:30880/TCP   15m
traefik-web-service         NodePort   10.32.0.187   <none>        80:30080/TCP     15m
```

Create an Ingress resource: `kubectl apply -f ingress.yaml`. Traefik will route HTTP from its `traefik-web-service` NodePort service to the Python HTTP service. So this works:

```
$ while true; do curl -H "X-Frobozz: $RANDOM" http://192.168.56.200:30080/python-http; sleep 1s; done
2022-09-10 22:37:18.238067 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:37:19.251029 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:37:20.264372 -- python-http-np7s2 -- 10.200.127.200
2022-09-10 22:37:21.277277 -- python-http-np7s2 -- 10.200.127.200
```
etc.

## DaemonSet Logs
```
Host: 192.168.56.200:30080
User-Agent: curl/7.68.0
Accept: */*
X-Forwarded-For: 192.168.56.1
X-Forwarded-Host: 192.168.56.200:30080
X-Forwarded-Port: 30080
X-Forwarded-Proto: http
X-Forwarded-Server: traefik-deployment-64bf888576-pwhcj
X-Frobozz: 24123
X-Real-Ip: 192.168.56.1
Accept-Encoding: gzip
10.200.127.200 - - [10/Sep/2022 22:37:52] "GET /python-http HTTP/1.1" 200 -
2022-09-10 22:37:52.985997 -- python-http-np7s2 -- 10.200.127.200
```

etc.

## Customize

As stated above, the DaemonSet defaults to HTTP port 80. To change that, edit `kustomization.yaml` with the values you want then re-apply the manifests to the cluster.

## Clean up
```
kubectl delete ns python-http
```
