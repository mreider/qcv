# nginx-gunicorn-flask

This repository contains files necessary for building a Docker image of
Nginx + Gunicorn + Flask.


### Base Docker Image

* [ubuntu:16.04](https://registry.hub.docker.com/_/ubuntu/)

Install [Docker](https://www.docker.com/).

```bash
docker run -d -p 5000:80 -t flask
```

After few seconds, open `http://qcv.space` to see the Flask app.
