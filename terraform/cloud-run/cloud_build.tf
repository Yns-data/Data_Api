resource "google_cloudbuild_trigger" "github_trigger" {
  name = "data-api-github-trigger"

  github {
    owner = var.github_owner
    name  = var.github_repo

    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"
}
