{{- define "app.fullname" -}}
{{- if eq .Release.Name .Chart.Name -}}
{{ .Release.Name }}
{{- else -}}
{{ printf "%s-%s" .Release.Name .Chart.Name }}
{{- end -}}
{{- end }}

{{- define "app.lables" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/part-of: {{ .Chart.Name }}
app.kubernetes.io/version: {{ .Chart.ApiVersion | quote }}
app.kubernetes.io/component: webserver
{{- end -}}
