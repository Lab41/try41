FROM lab41/dendrite-ungit
MAINTAINER Charlie Lewis <charliel@lab41.org>

# snap
RUN wget --no-check-certificate https://snap.stanford.edu/releases/Snap-2.2.zip; \
    unzip Snap-2.2.zip; \
    rm -rf Snap-2.2.zip; \
    cd Snap-2.2; make all; \
    mv /Snap-2.2 /usr/share/tomcat7/
