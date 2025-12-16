# Homework: Module 04 / Lesson 13 — FluxCD GitOps для course-app

## Репозиторій
- GitHub: `https://github.com/kyle332106/rd-fluxcd-lesson.git`
- Структура: `base/`, `overlays/development`, `overlays/production`, `clusters/my-cluster`

## Вимоги
- kubectl має бачити кластер (Rancher Desktop): `kubectl get nodes`
- Flux CLI встановлений  
  - Windows: `winget install FluxCD.Flux` або спершу Chocolatey/Scoop  
  - macOS/Linux: `brew install fluxcd/tap/flux`
- Dragonfly Operator ставимо окремо перед Flux (див. нижче)
- GitHub PAT з правом push  
  - Bash: `export GITHUB_TOKEN=<PAT>`  
  - PowerShell: `$env:GITHUB_TOKEN = '<PAT>'`

## Кроки
1) Клон (якщо треба):
   ```bash
   git clone https://github.com/kyle332106/rd-fluxcd-lesson.git
   cd rd-fluxcd-lesson
   ```
2) Dragonfly Operator (один раз):  
   Bash:
   ```bash
   kubectl create namespace dragonfly-system --dry-run=client -o yaml | kubectl apply -f -
   helm repo add jacobcolvin https://jacobcolvin.com/helm-charts
   helm repo update
   helm upgrade --install dragonfly-operator jacobcolvin/dragonfly-operator \
     -n dragonfly-system \
     --version 0.1.1 \
     --set crds.install=true
   ```
   PowerShell:
   ```powershell
   kubectl create namespace dragonfly-system --dry-run=client -o yaml | kubectl apply -f -
   helm repo add jacobcolvin https://jacobcolvin.com/helm-charts
   helm repo update
   helm upgrade --install dragonfly-operator jacobcolvin/dragonfly-operator `
     -n dragonfly-system `
     --version 0.1.1 `
     --set crds.install=true
   ```

3) Експорт PAT:
   - Bash: `export GITHUB_TOKEN=<PAT>`
   - PowerShell: `$env:GITHUB_TOKEN = '<PAT>'`

4) Bootstrap Flux:
   ```bash
   flux bootstrap github \
     --owner=kyle332106 \
     --repository=rd-fluxcd-lesson \
     --branch=main \
     --path=./clusters/my-cluster \
     --personal
   ```
   PowerShell (з бектіками):
   ```powershell
   flux bootstrap github `
     --owner=kyle332106 `
     --repository=rd-fluxcd-lesson `
     --branch=main `
     --path=./clusters/my-cluster `
     --personal
   ```

5) Перевірка:
   ```bash
   flux get kustomizations
   kubectl get ns development production
   kubectl get pods,svc,ingress -n development
   kubectl get pods,svc,ingress,hpa -n production
   kubectl get dragonfly -A
   ```

Drift-check: видаліть сервіс у production  
```bash
kubectl delete svc course-app -n production
```
Flux відновить його за ~хвилину.
