terraform {
  required_version = ">= 1.0"
  backend "local" {} // Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials) // Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dsid
  project    = var.project
  location   = var.region
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location      = var.region

  # Optional, but recommended settings:
  storage_class = var.storage_class

}