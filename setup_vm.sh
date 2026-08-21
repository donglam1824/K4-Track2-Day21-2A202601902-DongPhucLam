#!/bin/bash
cat << 'EOF' > income-api.service
[Unit]
Description=Income Model Inference Server
After=network.target

[Service]
User=dongl
WorkingDirectory=/home/dongl
Environment="ARTIFACT_BUCKET=income-lab-bucket-donglam-16"
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/dongl/sa-key.json"
ExecStart=/usr/bin/python3 /home/dongl/src/serve.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

gcloud compute scp income-api.service income-api:/tmp/income-api.service --zone=us-central1-a
gcloud compute ssh income-api --zone=us-central1-a --command="sudo mv /tmp/income-api.service /etc/systemd/system/income-api.service && sudo systemctl daemon-reload && sudo systemctl enable income-api"
