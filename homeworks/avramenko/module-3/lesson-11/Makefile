NAMESPACE=rd
CRT=./crt/course-app.local.crt
KEY=./crt/course-app.local.crt
RELEASE=vavr

lint:
	helm lint course-app ./course-app -f course-app/values.yaml --set-file tls.crt=$(CRT) --set-file tls.key=$(KEY) -n $(NAMESPACE)

template:
	helm template course-app -f course-app/values.yaml --set-file tls.crt=$(CRT) --set-file tls.key=$(KEY) -n $(NAMESPACE)

upgrade:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm dependency update course-app
	helm upgrade $(RELEASE) course-app -f course-app/values.yaml --set-file tls.crt=$(CRT) --set-file tls.key=$(KEY) -n $(NAMESPACE) --create-namespace -i

purge:
	kubectl delete namespaces rd
