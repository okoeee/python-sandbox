
## 仮想環境の作成

```sh
# 環境の作成
python3 -m venv [new_env_name]

# activate
source [new_env_name]/bin/activate

# deactivate
deactivate
```

## Credentialの設定
環境変数をTerminalに貼り付け
```sh
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```

## ファイル実行

```sh
# import 
pip install boto3

# 実行
python3 [file_name].py
```
