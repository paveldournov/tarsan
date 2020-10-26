REM expose KFP UI
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80

REM get GCP secret key
gcloud iam service-accounts keys create application_default_credentials.json \
  --iam-account [SA-NAME]@[PROJECT-ID].iam.gserviceaccount.com

REM install GCP secret
kubectl create secret -n [your-namespace] generic user-gcp-sa \
  --from-file=user-gcp-sa.json=application_default_credentials.json

