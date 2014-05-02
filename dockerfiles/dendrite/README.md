To get the environment for Dendrite on top of Docker you can either Pull it from the public docker index, or you can build it from source.

Pull from Docker index:
=======================
```
sudo docker pull lab41/dendrite
sudo docker tag lab41/dendrite dendrite
```

Build from source:
==================
```
git clone https://github.com/Lab41/try41.git
cd try41/dockerfiles/dendrite
sudo docker build -t dendrite .
```

Once the image has been built you can either run it as a contained webapp as it's used in Try41, or you can run in a shell and poke around.

Run as a webapp:
================
```
sudo docker run -d -P dendrite
```

Run in a shell:
===============
```
sudo docker run -i -t -P dendrite /bin/bash
```

NOTE: when running in a shell, you can also execute /usr/bin/supervisord and access the webapp from the exposed port

Find port that was exposed:
===========================
```
sudo docker ps
```
