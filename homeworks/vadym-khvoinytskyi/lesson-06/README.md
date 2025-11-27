## Docs to obtain credentials for github container registry

https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
https://github.com/settings/tokens/new?scopes=write:packages

## Commands to push course-app image to github container registry
export CR_PAT=YOUR_TOKEN
echo $CR_PAT | docker login ghcr.io -u VadymKhvoinytskyi --password-stdin
docker image push ghcr.io/vadymkhvoinytskyi/course-app:latest


## Kubernetes commands neccessary to deploy course-app

k apply -f namespace.yaml
k config set-context --current --namespace=rd
k create secret docker-registry github --docker-server=ghcr.io --docker-username=vadymkhvoinytskyi --docker-password=<access_token>
k apply -f deployment.yaml
k scale --replicas=3 deployment course-app -n rd
k rollout status deployment/course-app
