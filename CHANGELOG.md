## 1.2.0

Fork https://github.com/wastrachan/docker-gandi-ddns
Use ubi with s2i
Convert the image to use it in kubernetes
Make it compatible with security standard to be able to run on OCP


## 1.2

Update dependencies
Update base image to latest python3.12 alpine
Format code with black

## 1.1.1

Update requests to 2.28.0
Update base image to latest python3.10 alpine

## 1.1

Added caching for public addresses to avoid unneeded updates to the Gandi API.

## 1.0

Initial release of Gandi Dynamic DNS.
