docker build -t portal . --no-cache
docker tag portal gcr.io/cidc-dfci/portal:dev
docker push gcr.io/cidc-dfci/portal:dev
