resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.api.name

  role   = "roles/run.invoker"
  member = "allUsers"
}


##################################
# Cloud Run service
##################################
resource "google_cloud_run_v2_service" "api" {
  name     = var.service_name
  location = var.region

  template {
    service_account = var.runtime_sa
    timeout         = "300s"

  
    
    scaling {
      max_instance_count = 10
      min_instance_count = 1
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/data-api/fastapi-app:${var.image_tag}"

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      env {
        name  = "DATA_API_KEY_NAME"
        value = "access_token"
      }

      env {
        name = "DATA_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "DATA_API_KEY"
            version = "latest"
          }
        }
      }
    }
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }

  ingress = "INGRESS_TRAFFIC_ALL"
}
