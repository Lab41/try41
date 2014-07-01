try41
==============

try41 is a demonstration platform tailored to demonstration three projects Lab41 has worked on.  try41 leverages Docker through a simple webapp to enable on-demand instances of isolated installations of each project.

In order to run [try41](https://github.com/Lab41/try41), on a host with docker perform the following:

```
docker run -d -p 6379:6379 lab41/redis
```

```
SECRET_KEY="this is my secret key"

docker run -e SUBDOMAIN=`hostname -f` \
           -e REDIS_HOST=`hostname -f` \
           -e SECRET_KEY=$SECRET_KEY \
           -e USERS=False \
           -d -P lab41/try41
```

This will give you a webapp through an exposed port chosen by Docker that will describe each project and provide you the ability to launch each project as a new Docker container.

The try41 webapp can also be launched to use user accounts.  In that case, you'll first need to also spin up an additional container for PostgreSQL:

```
docker run -d -p 5432:5432 lab41/postgresql
```

You will also need an SMTP server to send mail from for registration.

Then modify the runtime environment variables to enable users:

```
SECRET_KEY="this is my secret key"
HOSTNAME=hostname -f

docker run -e SUBDOMAIN=`hostname -f` \
           -e REDIS_HOST=`hostname -f` \
           -e SECRET_KEY=$SECRET_KEY \
           -e USERS=True \
           -e POSTGRESQL_URI=postgresql://docker:docker@$HOSTNAME/users \
           -e MAIL_HOST=smtp.example.com \
           -e SENDER='"Try41" <noreply@example.com>' \
           -d -P lab41/try41
```

Before launching each project, you will want to pull down their images with Docker.

**To get [Dendrite](https://github.com/Lab41/Dendrite):**
```
docker pull lab41/dendrite
```

Or build from source:

```
git clone https://github.com/Lab41/try41.git

cd try41/dockerfiles/dendrite
./build.sh
```

**To get [Hemlock](https://github.com/Lab41/Hemlock):**
```
docker pull lab41/hemlock
```

Or build from source:

```
git clone https://github.com/Lab41/try41.git

cd try41/dockerfiles/hemlock

docker build -t lab41/hemlock .
```

**To get [Redwood](https://github.com/Lab41/Redwood):**
```
docker pull lab41/redwood
```

Or build from source:

```
git clone https://github.com/Lab41/try41.git

cd try41/dockerfiles/redwood

docker build -t lab41/redwood .
```
