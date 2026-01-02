resource "google_artifact_registry_repository" "cloud_run" {
  location      = var.region
  repository_id = "cloud-run"
  format        = "DOCKER"
}
