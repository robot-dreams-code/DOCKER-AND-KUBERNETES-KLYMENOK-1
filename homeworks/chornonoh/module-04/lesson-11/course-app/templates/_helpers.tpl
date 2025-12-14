{{- define "course-app.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "course-app.fullname" -}}
{{ include "course-app.name" . }}-{{ .Release.Name }}
{{- end }}

{{/*
Return Redis hostname depending on internal/external config
*/}}
{{- define "course-app.redisHost" -}}
{{- if .Values.redis.internal.enabled -}}
{{ include "course-app.fullname" . }}-redis
{{- else -}}
{{ .Values.redis.external.host }}
{{- end -}}
{{- end }}

{{/*
Return Redis port depending on internal/external config
*/}}
{{- define "course-app.redisPort" -}}
{{- if .Values.redis.internal.enabled -}}
6379
{{- else -}}
{{ .Values.redis.external.port }}
{{- end -}}
{{- end }}

