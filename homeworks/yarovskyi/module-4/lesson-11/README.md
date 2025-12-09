# Lesson 11 Helm

1. Add redis repo:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency update ./homeworks/yarovskyi/module-4/lesson-11/course-app
```

2. Check templates:
```bash
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/configmap.yaml
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/secret.yaml
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/deployment.yaml
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/hpa.yaml
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/service.yaml
helm template course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app --show-only templates/ingress.yaml
```

3. Install helm chart:
```bash
helm upgrade --install course-app ./homeworks/yarovskyi/module-4/lesson-11/course-app -n robotdreams --create-namespace
```

Check https://course-app.local

4. Uninstall helm chart:
```bash
helm uninstall course-app -n robotdreams
```
