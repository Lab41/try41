#!/bin/bash

cd dendrite-build
docker build -t lab41/dendrite-build .
cd ../dendrite-java
docker build -t lab41/dendrite-java .
cd ../dendrite-cdh5
docker build -t lab41/dendrite-cdh5 .
cd ../dendrite-elasticsearch
docker build -t lab41/dendrite-elasticsearch .
cd ../dendrite-graphlab
docker build -t lab41/dendrite-graphlab .
cd ../dendrite-snap
docker build -t lab41/dendrite-snap .
cd ../dendrite-repos
docker build -t lab41/dendrite-repos .
cd ../dendrite-ungit
docker build -t lab41/dendrite-ungit .
cd ..
docker build -t lab41/dendrite .
