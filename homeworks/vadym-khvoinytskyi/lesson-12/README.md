
## To get official dragonfly operator helm chart
download https://github.com/dragonflydb/dragonfly-operator/tree/main/charts/dragonfly-operator to local dir

## To use dragonfly with course-app

Change APP_REDIS_URL: redis://redis:6379/0 to APP_REDIS_URL: redis://dragonfly:6379/0 


## Apply yamls in RBAC folder and check accounts rights

✗ kubectl auth can-i list dragonflies --as=system:serviceaccount:rd:db-viewer
yes

✗ kubectl auth can-i delete dragonflies --as=system:serviceaccount:rd:db-viewer
no
