#!/bin/bash

# CloudWatch Logs エージェントのインストール
sudo yum install -y amazon-cloudwatch-agent

# dockerのログとしてCloudWatchを認知させるための設定
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "ap-northeast-1"
    "awslogs-group": "backoffice-bot-log"
  }
}
EOF

echo "CloudWatch Logs agent setup complete. Please setup IAM role for CloudWatch Logs."
