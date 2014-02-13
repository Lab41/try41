from ubuntu
MAINTAINER Charlie Lewis <charliel@lab41.org>

ENV REFRESHED_AT 2014-02-13
RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

# Keep upstart from complaining
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN apt-get install -y git
RUN git clone https://github.com/Lab41/try-challenges.git
RUN apt-get install -y python-setuptools
RUN easy_install pip
RUN pip install -r /try-challenges/requirements.txt

EXPOSE 5000

CMD ["python", "/try-challenges/api.py"]
