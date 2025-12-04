{{/*
Expand the name of the chart.
*/}}
{{- define "course-app.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "course-app.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}
