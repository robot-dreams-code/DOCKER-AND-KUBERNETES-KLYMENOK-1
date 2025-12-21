:: 1) Має бути "yes"
kubectl auth can-i list dragonflies -n course-app --as=system:serviceaccount:course-app:db-viewer

:: 2) Має бути "no"
kubectl auth can-i delete dragonflies -n course-app --as=system:serviceaccount:course-app:db-viewer