{{/*
Fullname (release-prefixed chart name)
*/}}
{{- define "eoip.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{ .Values.fullnameOverride }}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end }}

{{/*
Common labels
*/}}
{{- define "eoip.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | quote }}
{{ include "eoip.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "eoip.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Component selector labels
*/}}
{{- define "eoip.componentLabels" -}}
{{ include "eoip.selectorLabels" .root }}
app.kubernetes.io/component: {{ .component }}
{{- end }}

{{/*
Full image reference
*/}}
{{- define "eoip.image" -}}
{{- if .Values.image.registry -}}
{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}
{{- else -}}
{{ .Values.image.repository }}:{{ .Values.image.tag }}
{{- end -}}
{{- end }}

{{/*
HA podAntiAffinity block for a component. Usage:
  {{- include "eoip.podAntiAffinity" (dict "root" . "component" "api" "cfg" .Values.api) }}
*/}}
{{- define "eoip.podAntiAffinity" -}}
{{- if and .cfg.podAntiAffinity .cfg.podAntiAffinity.enabled }}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: {{ .root.Chart.Name }}
            app.kubernetes.io/instance: {{ .root.Release.Name }}
            app.kubernetes.io/component: {{ .component }}
        topologyKey: {{ .cfg.podAntiAffinity.topologyKey | default "kubernetes.io/hostname" }}
{{- end }}
{{- end }}
