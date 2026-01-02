resource "google_cloud_run_v2_service" "api" {
  name     = var.service_name
  location = var.region

  template {
    service_account = var.runtime_sa
    timeout         = "300s"

    containers {
      image = "europe-west9-docker.pkg.dev/${var.project_id}/cloud-run/data-api:latest"

      container_concurrency = 80

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

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image
    ]
  }
}
