import boto3
from datetime import datetime, timedelta

# セッションの初期化
session = boto3.Session()

# CloudWatch クライアントの作成
cloudwatch = session.client('cloudwatch')

# メトリクス取得のパラメータ設定
def main():
  response = cloudwatch.get_metric_statistics(
    Namespace='AWS/ECS',
    MetricName='CPUUtilization',
    Dimensions=[
      {
        'Name': 'ClusterName',
        'Value': 'app-cluster-asp-kidsna-com'  # クラスター名を指定
      },
      {
        'Name': 'ServiceName',
        'Value': 'connect-api-v2-with-sd'  # サービス名を指定
      }
    ],
    StartTime=datetime.utcnow() - timedelta(minutes=60),  # 過去1時間のデータ
    EndTime=datetime.utcnow(),
    Period=60,  # ◯秒間隔
    Statistics=['Average']
  )

  for data_point in response['Datapoints']:
      print(f"Time: {data_point['Timestamp']}, CPU Usage: {data_point['Average']}%")

if __name__ == "__main__":
    main()
