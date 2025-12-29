resource "google_cloud_run_v2_service_iam_member" "public" {
  name     = google_cloud_run_v2_service.api.name
  location = google_cloud_run_v2_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
resource "google_project_iam_member" "cloudbuild_run_admin" {
  role   = "roles/run.admin"
  member = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_sa_user" {
  role   = "roles/iam.serviceAccountUser"
  member = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}
