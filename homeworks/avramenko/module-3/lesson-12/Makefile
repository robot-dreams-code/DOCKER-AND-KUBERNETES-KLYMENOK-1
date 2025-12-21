install:
	kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
	kubectl apply -f ./manifests/namespace.yaml
	kubectl apply -f ./manifests

purge:
	kubectl delete namespaces rd
	kubectl delete namespaces dragonfly-operator-system

check:
	kubectl auth can-i list dragonflies --as=system:serviceaccount:rd:db-viewer -n dragonfly-operator-system
	kubectl auth can-i delete dragonflies --as=system:serviceaccount:rd:db-viewer -n dragonfly-operator-system
