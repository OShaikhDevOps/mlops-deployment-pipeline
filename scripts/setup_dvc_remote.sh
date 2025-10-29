#!/usr/bin/env bash
# Example helper to configure a DVC S3 remote. Run locally after installing AWS CLI and configuring credentials.

set -euo pipefail

# Usage: ./scripts/setup_dvc_remote.sh <s3-bucket-name> <remote-name>
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <s3-bucket-name> <remote-name>"
  exit 1
fi

BUCKET=$1
REMOTE_NAME=$2

# Create remote in DVC config
# dvc remote add -d ${REMOTE_NAME} s3://${BUCKET}/dvcstore
# dvc remote modify ${REMOTE_NAME} endpointurl https://s3.amazonaws.com

cat <<EOF
Run these commands to configure DVC remote:
  dvc remote add -d ${REMOTE_NAME} s3://${BUCKET}/dvcstore
  dvc remote modify ${REMOTE_NAME} endpointurl https://s3.amazonaws.com
  dvc push

Ensure AWS credentials are configured and the bucket exists.
EOF
