variable "project" {
  description = "Your GCP Project ID"
  default     = "blah-blah-blah"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-central1"
  type        = string
}

variable "credentials" {
  description = "Credentials file location"
  default     = "./blah-bot-blah-blah.json"
}

variable "dsid" {
  description = "Dataset ID"
  default     = "example_dataset"
}