#!/bin/bash

echo 'This image should be used using crontab, you can read it on `https://github.com/ccordoui/container-gandi-ddns/blob/stable/README.md`'
echo
echo 'Here is a configuration exemple:'
echo

cat <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: gandi-ddns
spec:
  schedule: "*/15 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: gandi-ddns
            image: quay.io/ccordoui/container-gandi-ddns:latest
            imagePullPolicy: Always
            concurrencyPolicy: Replace
            restartPolicy: Never
            command:
            - python3
            - gandi-ddns.py
          restartPolicy: OnFailure
          envFrom:
            - configMapRef:
                name: gandi-ddns
            - secretRef:
                name: gandi-ddns
EOF

exit 1
