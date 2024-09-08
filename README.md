# Gandi Dynamic DNS

Dynamic DNS Update Client for Gandi's LiveDNS.

[![](https://circleci.com/gh/wastrachan/docker-gandi-ddns.svg?style=svg)](https://circleci.com/gh/wastrachan/docker-gandi-ddns)
[![](https://img.shields.io/docker/pulls/wastrachan/gandi-ddns.svg)](https://hub.docker.com/r/wastrachan/gandi-ddns)

## Install

#### Docker Hub

Pull the latest image from Quay:

```bash
podman pull quay.io/ccordoui/container-gandi-ddns
```

#### Build From Source

Clone this repository, and run `buildah bud -t container-gandi-ddns .` to build an image:

```bash
git clone https://github.com/ccordoui/container-gandi-ddns.git
cd container-gandi-ddns
buildah bud -t container-gandi-ddns .
```

## Run

## Configuration

Configuration is accomplished through the use of environment variables.

```yaml
# cm.yaml
--- 
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  GANDI_DOMAIN: "example.com"
  GANDI_RECORD: "www"
---
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: gandi-ddns
data:
  GANDI_TOKEN: "My Secret Token"
```

## Run

Deploy a crontab in kubernetes:
```yaml
---
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: gandi-ddns
spec:
  schedule: "*/15 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: gandi-ddns
            image: quay.io/ccordoui/container-gandi-ddns:stable
            imagePullPolicy: Always
            command:
            - python3
            - gandi-ddns.py
          restartPolicy: OnFailure
          envFrom:
            - configMapRef:
                name: gandi-ddns
            - secretRef:
                  name: gandi-ddns
```

#### Environment Variables
    cache = Cache(Path(os.environ.get('CACHE_PATH', '/dev/shm')))
    url = os.environ.get("GANDI_URL", "https://dns.api.gandi.net/api/v5/")
    token = os.environ.get("GANDI_TOKEN", '')
    domain = os.environ.get("GANDI_DOMAIN")
    record = os.environ.get("GANDI_RECORD", "@")
    protocols = os.environ.get("PROTOCOLS", 'ipv4,ipv6').split(',')

| Variable          | Default                             | Description                                                                                          |
| ----------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `CACHE_PATH`      | `/dev/shm`                          | The base path for the ip cache (can be on PV, but in memory is enough for most scenarios             |
| `GANDI_URL`       | `https://dns.api.gandi.net/api/v5`  | URL of the Gandi API.                                                                                |
| `GANDI_TOKEN`     | -                                   | API Key for your [Gandi.net account](https://docs.gandi.net/en/domain_names/advanced_users/api.html) |
| `GANDI_DOMAIN`    | -                                   | Your Gandi.net domain name                                                                           |
| `GANDI_RECORD`    | `@`                                 | Record to update with your IP address                                                                |
| `PROTOCOLS`       | `ipv4,ipv6`                         | What need to be updated (can be `ipv4`, `ipv6` or `ipv4,ipv6`                                        |

## License

The content of this project itself is licensed under the [MIT License](LICENSE).
