REGISTRY=vitaliyavramenko
IMAGE_NAME=lesson-6
TAG=latest

build:
	cp -r ../../../../apps/course-app docker/
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(TAG) docker/
	rm -r docker/course-app

push:
	docker push $(REGISTRY)/$(IMAGE_NAME):$(TAG)

run:
	docker run -d -p 8080:8080 $(REGISTRY)/$(IMAGE_NAME):$(TAG)

produce: build push

stop:
	docker stop $$(docker ps -q --filter ancestor=$(REGISTRY)/$(IMAGE_NAME):$(TAG)) 2>/dev/null || true

deploy:
	kubectl apply -f ./manifests/deployment.yaml
