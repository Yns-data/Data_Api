output "cloud_run_url" {
  description = "URL publique Cloud Run"
  value       = google_cloud_run_v2_service.api.uri
}
