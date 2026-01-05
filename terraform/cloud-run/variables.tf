variable "project_id" {
  description = "ID du projet GCP "
  type        = string
}

variable "region" {
  description = "Région GCP"
  type        = string
  default     = "europe-west9"
}

variable "service_name" {
  description = "Nom du service Cloud Run"
  type        = string
  default     = "api-source-1"
}

variable "runtime_sa" {
  description = "Service Account utilisé par Cloud Run ET Cloud Build"
  type        = string
}

variable "image_tag" {
  description = "Tag de l'image Docker"
  type        = string
}