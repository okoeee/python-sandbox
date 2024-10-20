import boto3
import time

# セッションの初期化
session = boto3.Session(profile_name='ecs-full-access-user')
ecs = session.client('ecs')

# クラスターをリスト化して選択する関数
def list_clusters():
    clusters = ecs.list_clusters()
    cluster_arns = clusters['clusterArns']
    print("Select a cluster:")
    for idx, cluster in enumerate(cluster_arns):
        print(f"{idx}: {cluster}")
    selected_idx = int(input("Enter the number of the cluster: "))
    return cluster_arns[selected_idx]

# サービスをリスト化して選択する関数
def list_services(cluster_arn):
    services = ecs.list_services(cluster=cluster_arn)
    service_arns = services['serviceArns']
    print("Select a service:")
    for idx, service in enumerate(service_arns):
        print(f"{idx}: {service}")
    selected_idx = int(input("Enter the number of the service: "))
    return service_arns[selected_idx]

# タスクをリスト化して選択する関数
def list_tasks(cluster_arn):
    tasks = ecs.list_tasks(cluster=cluster_arn)
    task_arns = tasks['taskArns']
    print("Select a task:")
    for idx, task in enumerate(task_arns):
        print(f"{idx}: {task}")
    selected_idx = int(input("Enter the number of the task: "))
    return task_arns[selected_idx]

# タスクの現在のCPUとメモリを表示する関数
def describe_task(cluster_arn, task_arn):
    task = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])
    container = task['tasks'][0]['containers'][0]['containerArn']
    print(f"Current specs for {container}")
    # タスク定義のCPUとメモリを取得（ダミーの例として使用、実際にはタスク定義の情報を取得する必要があります）
    task_definition_arn = task['tasks'][0]['taskDefinitionArn']
    task_def = ecs.describe_task_definition(taskDefinition=task_definition_arn)
    cpu = task_def['taskDefinition']['cpu']
    memory = task_def['taskDefinition']['memory']
    print(f"CPU: {cpu}, Memory: {memory}")
    return cpu, memory, task_definition_arn

# タスク定義を新しいCPUとメモリで更新する関数
def update_task_definition(task_definition_arn, new_cpu, new_memory):
    # 現在のタスク定義を取得
    response = ecs.describe_task_definition(taskDefinition=task_definition_arn)
    
    task_def = response['taskDefinition']
    
    # コンテナ定義を取得し、CPUやメモリの設定を変更
    container_definitions = task_def['containerDefinitions']
    
    for container_def in container_definitions:
        # コンテナのリソース制約を変更する
        container_def['cpu'] = int(new_cpu)  # 必要に応じてCPUを変更
        container_def['memory'] = int(new_memory)  # 必要に応じてメモリを変更
    
    # 新しいタスク定義を作成（ファミリーやその他のプロパティを保持しつつ）
    new_task_def = ecs.register_task_definition(
        family=task_def['family'],  # ファミリー名は同じ
        taskRoleArn=task_def.get('taskRoleArn'),
        executionRoleArn=task_def.get('executionRoleArn'),
        networkMode=task_def['networkMode'],
        containerDefinitions=container_definitions,  # 更新されたコンテナ定義
        volumes=task_def['volumes'],
        placementConstraints=task_def.get('placementConstraints'),
        requiresCompatibilities=task_def['requiresCompatibilities'],
        cpu=str(new_cpu),  # タスク全体のCPUを指定
        memory=str(new_memory),  # タスク全体のメモリを指定
        runtimePlatform=task_def.get('runtimePlatform')
    )

    print("New task definition created:", new_task_def['taskDefinition']['taskDefinitionArn'])
    return new_task_def['taskDefinition']['taskDefinitionArn']


# サービスを新しいタスク定義で更新する関数
def update_service(cluster_arn, service_arn, task_definition_arn):
    response = ecs.update_service(
        cluster=cluster_arn,
        service=service_arn,
        taskDefinition=task_definition_arn
    )
    print(f"Updated service {service_arn} to use new task definition {task_definition_arn}")

# 指定した時間経過後に元のCPUとメモリ設定に戻す関数
def revert_specs(cluster_arn, service_arn, original_cpu, original_memory, original_task_definition, duration):
    print(f"Reverting specs back after {duration} minutes...")
    time.sleep(duration * 60)  # 指定した分数だけ待機
    task_definition_arn = update_task_definition(original_task_definition, original_cpu, original_memory)
    update_service(cluster_arn, service_arn, task_definition_arn)
    print("Reverted specs to original.")

# メイン処理
def main():
    cluster_arn = list_clusters()  # クラスターを選択
    service_arn = list_services(cluster_arn)  # サービスを選択
    task_arn = list_tasks(cluster_arn)  # タスクを選択
    
    # 現在のCPUとメモリ、タスク定義を取得
    original_cpu, original_memory, original_task_definition = describe_task(cluster_arn, task_arn)
    
    # 新しいCPUとメモリの値を入力
    new_cpu = input("Enter new CPU value: ")
    new_memory = input("Enter new Memory value: ")
    
    # 新しいCPUとメモリでタスク定義を更新
    new_task_definition_arn = update_task_definition(original_task_definition, new_cpu, new_memory)
    
    # サービスを新しいタスク定義で更新
    update_service(cluster_arn, service_arn, new_task_definition_arn)
    
    # 一定時間経過後に元の設定に戻す
    duration = int(input("Enter the duration in minutes to keep the new specs: "))
    revert_specs(cluster_arn, service_arn, original_cpu, original_memory, original_task_definition, duration)

if __name__ == "__main__":
    main()
