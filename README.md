# Python HTTP/s Server DaemonSet

Minimal HTTP/HTTPS server for testing connectivity for Ingresses, Load Balancers, etc.

## Quick Start

`helm upgrade --install python-http python-http --namespace python-http --create-namespace`

(By default this creates an Ingress with ingress class `nginx`.)

## Test:

Here's a hypothetical output of `kubectl get nodes -owide`:
```
NAME  STATUS  ROLES              AGE   VERSION  INTERNAL-IP     ...
vm1   Ready   controller,worker  7d1h  v1.29.2  192.168.122.61  ...
vm2   Ready   worker             7d1h  v1.29.2  192.168.122.129 ...
vm3   Ready   worker             7d1h  v1.29.2  192.168.122.226 ...
```

Then:
```
curl -k https://192.168.122.61/python-http
```

Output:
```
2024-03-31 23:10:01.792762 -- python-http-54xsq -- 192.168.122.1
```
## Values

| Value | Default | Description |
|-|-|-|
| `ingress.enabled` | `true` | Ingress is enabled by default. |
| `ingress.className` | `nginx` | Nginx is the default ingress class |
| `service.type` | `ClusterIP` | Default service type. |
| `service.port` | `80` | Default service port. |
| `isHttps` | `true` | Serves HTTPS by default. (Creates a self-signed cert.) |
| `nodeport` | `false` | Does not create a `NodePort` service by default. |
