# Notes from Week 1

## Terraform and GCP

Time to get up in the clouds! Using Google Cloud Platform since the free account comes with $300 woth of free credits.

### GCP Setup Stuff

Create an account on GCP. Setup a new project and write down the Project ID. Also create a Service Account from ``IAM & Admin`` section and download the authentication keys. 

- A _service account_ is a user account that you never really log into for apps and workloads; you may authorize or limit what resources are available to your apps with service accounts based on various roles. You can also make custom roles or just work with Google's roles.

- Select the 3 dots or ellipses on the created user and go to _Manage Keys_. Create a new key in `.json` format. The file will be downloaded automatically.

If you want to add more roles later, navigate to the `IAM` tab under the `IAM & Admin` section.

Download Google Cloud SDK and when you run `gcloud init`, it will ask you to login and let you select a project that you want to work on. 

### OAuth Authentication to your GCP:

Assign global varibale for google authentication key by running below code:
```bash
        export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"
```


Refresh the token and verify with GCP SDK:
```bash
        gcloud auth application-default login
```

We will be using BigQuery and need somewhere to store the data. Go to `IAM` section and click on the _service account_ to add more roles so the service account can access them. Add the following roles.
    * `Storage Admin`: to create and manage _buckets_ (this is where raw data will be stored; data lake).
    * `Storage Object Admin`: to create and manage _objects_ in a bucket.
    * `BigQuery Admin`: to create and manage BigQuery resources and data.

Enable these APIs. Open the link and add them but be sure to be on the project. Terraform uses these APIs to interact with GCP:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com


### Terraform 

Infrastructure as Code

- Terraform is basically used to bypass any cloud services GUI and it has source control, version control and is made in mind with the best practices of DevOps.
- Terraform configuration files can be in `.tf` or `tf.json` for JSON files. There should be only one configuration file in the working directory. 
- Usually there is a `main.tf` file and a `variables.tf` file. 
- It is kinda like a docker-compose for cloud. 

### Why Terraform?

- Easy to keep track of your infrastructure. (size of disk, type of storage, what is being made all in a file)
- Easy to collaborate. (since it is one file you can upload it to GitHub and collab)
- Easy to reproduce. (using the file in another VM or machine to recreate)
- Reduce resource consumption. (Once you are done you can remove everything you build easily with one command)

The only terraform commands mostly needed:
    * `terraform fmt` : formats your configuration files in the right way.
    * `terraform validate` : check if configuration is valid other throws out an error.
    * `terraform init` : initialize by downloading mentioned providers/plugins.
    * `terraform plan` :  Only displays the changes that will be applied to the remote state in GCP.
    * `terraform apply` : applies the changes.
    * `terraform destroy` : destroys everything that terraform build from the cloud infrastructure.



Let's look at the a basic `main.tf` terraform script and disect it.

```json
terraform {
  required_version = ">= 1.0"
  backend "local" {}  // Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  zone   = var.zone
  credentials = file(var.credentials)  // Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dbid
  project    = var.project
  location   = var.region
}
```
It uses simple block-style codes with 3 blocks, so let's run through it block by block.

```json
terraform {
  required_version = ">= 1.0"
  backend "local" {} 
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}
```
There must only be one `terraform` block but there can be multiple `provider` and `resource` blocks.
- The `terraform` block will run when you `terraform init`. 
- Specify required version; not required.
- `backend` is where to save the `.tfstate` file.
- `required_providers` is which providers needed to be used. Here it is just one but we can use multiple. Another advantage of terraform.

```json
provider "google" {
  project = var.project
  region = var.region
  zone   = var.zone
  credentials = file(var.credentials)  
}
```
Pretty straight-forward, just added the settings for GCP provider. Project name, region name, zone and credentials to connect to GCP (service account key). Note here there is something called `var.<name>`. Variabels from ``variable.tf`` which will be looked at after the next block.

Lets look at how to define Terraform variable within `variable.tf` file:
```json
variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-central1"
  type        = string
}
```
- `region` is obviously the variable name and the parameters for the variables are within the curly brackets. 
- `type` is optional. 
- `default` is what the value will be unless edited

You can look at Terraforms documentation to know more about what providers and parameters are available and also how to use them. (`Ctl+F` is your friend)







