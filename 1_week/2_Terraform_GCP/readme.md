# Notes from Week 1

## Terraform and GCP

Time to get up in the clouds! Using Google Cloud Platform since the free account comes with $300 woth of free credits.

- Terraform is basically used to bypass any cloud services GUI and it has source control, version control and is made in mind with the best practices of DevOps.

### GCP Setup Stuff

Create an account on GCP. Setup a new project and write down the Project ID. Also create a Service Account from ``IAM & Admin`` and download the authentication keys. 

- A _service account_ is a user account for apps and workloads; you may authorize or limit what resources are available to your apps with service accounts based on various roles. You can also make custom roles or just work with Google's roles.

- Select the 3 dots or ellipses on the created user and go to _Manage Keys_. Create a new key in `.json` format. The file will be downloaded automatically.

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

