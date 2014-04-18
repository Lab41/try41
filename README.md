try41
==============

try41 is a demonstration platform tailored to demonstration three projects Lab41 has worked on.  try41 leverages Docker through a simple webapp to enable on-demand instances of isolated installations of each project.

In order to run [try41](https://github.com/Lab41/try41), on a host with docker perform the following:

```
docker run -e SUBDOMAIN=`hostname -f` -d -P lab41/try41
```

This will give you a webapp through an exposed port chosen by Docker that will describe each project and provide you the ability to launch each project as a new Docker container.

Before launching each project, you will want to pull down their images and tag them with Docker.

**To get [Dendrite](https://github.com/Lab41/Dendrite):**
```
docker pull lab41/dendrite
docker tag lab41/dendrite dendrite
```

Note: The build on index.docker.io has been behind the GitHub repo, so to get the latest and greatest do this instead:

```
git clone https://github.com/Lab41/try41.git
cd try41/dockerfiles/dendrite
docker build .
docker tag [IMAGE_ID] dendrite
```

**To get [Hemlock](https://github.com/Lab41/Hemlock):**
```
docker pull lab41/hemlock
docker tag lab41/hemlock hemlock
```

Note: The build on index.docker.io has been behind the GitHub repo, so to get the latest and greatest do this instead:

```
git clone https://github.com/Lab41/try41.git
cd try41/dockerfiles/hemlock
docker build .
docker tag [IMAGE_ID] hemlock
```

**To get [Redwood](https://github.com/Lab41/Redwood):**
```
docker pull lab41/redwood
docker tag lab41/redwood redwood
```
