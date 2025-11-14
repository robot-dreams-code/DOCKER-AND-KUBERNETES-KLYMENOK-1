.PHONY: build-optimize
build-optimize:
	docker build -t calc-optimize:0.1 --build-arg A=9 --build-arg B=101 -f Optimize/Dockerfile .

.PHONY: build-not-optimize
build-not-optimize:
	docker build -t calc-not-optimize:0.1 --build-arg A=8 --build-arg B=321 -f NotOptimize/Dockerfile .

.PHONY: run-optimize
run-optimize:
	docker run --rm calc-optimize:0.1

.PHONY: run-not-optimize
run-not-optimize:
	docker run --rm calc-not-optimize:0.1

.PHONY: build-entrypoint-example
build-entrypoint-example:
	docker build -t entrypoint-example:0.1 -f Entrypoint/Dockerfile Entrypoint

.PHONY: run-entrypoint-example
run-entrypoint-example:
	docker run --rm entrypoint-example:0.1 -f Entrypoint/Dockerfile Entrypoint

.PHONY: run-entrypoint-example
run-entrypoint-example:
	docker run --rm entrypoint-example:0.1 -f Entrypoint/Dockerfile Entrypoint

.PHONY: build-user-example
build-user-example:
	docker build -t user:0.1 -f User/Dockerfile User

.PHONY: run-user-example
run-user-example:
	docker run --name user-example --rm -p 8080:8080 user:0.1

.PHONY: exec-user-example
exec-user-example:
	docker exec -it user-example bash
