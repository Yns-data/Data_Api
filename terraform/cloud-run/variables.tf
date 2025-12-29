variable "project_id" {
  type        = string
  description = "ID du projet GCP"
}

variable "region" {
  type    = string
  default = "europe-west9"
}

variable "service_name" {
  type    = string
  default = "api-source"
}

variable "github_owner" {
  type    = string
  default = "Yns-data"
}

variable "github_repo" {
  type    = string
  default = "Data_Api"
}

variable "service_account" {
  type        = string
  description = "Service account Cloud Run"
}
