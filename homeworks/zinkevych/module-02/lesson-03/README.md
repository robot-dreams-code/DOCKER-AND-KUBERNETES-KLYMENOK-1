# Building image from project root
`docker build -f homeworks/zinkevych/module-02/lesson-03/Dockerfile -t go-multi-stage .`

# Build only "build" stage
`docker build -f homeworks/zinkevych/module-02/lesson-03/Dockerfile --target build -t go-multi-stage-build .`

# Run container on port 8080
`docker run -p 8080:8080 go-multi-stage `

# Check non-root user
`docker run -it --entrypoint /bin/sh go-multi-stage`
`ls -l`
`whoami`
`id`
`touch test`

# Docker HUB
- Created report at Docker HUB
tag local image with remote key:
`docker tag go-multi-stage iozeen/go-multi-stage`
login to docker:
`docker login`
push linked image to HUB:
`docker push iozeen/go-multi-stage`
repo link:
https://hub.docker.com/repository/docker/iozeen/go-multi-stage/general
pull image:
`docker pull iozeen/go-multi-stage`