import boto3
import time

ecs = boto3.client('ecs')

def list_clusters():
    clusters = ecs.list_clusters()
    cluster_arns = clusters['clusterArns']
    print("Select a cluster:")
    for idx, cluster in enumerate(cluster_arns):
        print(f"{idx}: {cluster}")
    selected_idx = int(input("Enter the number of the cluster: "))
    return cluster_arns[selected_idx]

def list_tasks(cluster_arn):
    tasks = ecs.list_tasks(cluster=cluster_arn)
    task_arns = tasks['taskArns']
    print("Select a task:")
    for idx, task in enumerate(task_arns):
        print(f"{idx}: {task}")
    selected_idx = int(input("Enter the number of the task: "))
    return task_arns[selected_idx]

def describe_task(cluster_arn, task_arn):
    task = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])
    container = task['tasks'][0]['containerInstanceArn']
    print(f"Current specs for {container}:")
    # Show current CPU and memory (dummy example, you need to adjust it to actual task structure)
    cpu = task['tasks'][0]['cpu']
    memory = task['tasks'][0]['memory']
    print(f"CPU: {cpu}, Memory: {memory}")
    return cpu, memory

def update_task_definition(cluster_arn, task_arn, new_cpu, new_memory):
    # Example to update task definition or service
    ecs.update_service(
        cluster=cluster_arn,
        taskDefinition=task_arn,
        cpu=new_cpu,
        memory=new_memory
    )
    print("Updated the task definition")

def revert_specs(cluster_arn, task_arn, original_cpu, original_memory, duration):
    print(f"Reverting specs back after {duration} minutes...")
    time.sleep(duration * 60)  # wait for the specified duration
    update_task_definition(cluster_arn, task_arn, original_cpu, original_memory)
    print("Reverted specs to original.")

def main():
    cluster_arn = list_clusters()
    task_arn = list_tasks(cluster_arn)
    original_cpu, original_memory = describe_task(cluster_arn, task_arn)
    
    new_cpu = input("Enter new CPU value: ")
    new_memory = input("Enter new Memory value: ")
    update_task_definition(cluster_arn, task_arn, new_cpu, new_memory)

    duration = int(input("Enter the duration in minutes to keep the new specs: "))
    revert_specs(cluster_arn, task_arn, original_cpu, original_memory, duration)

if __name__ == "__main__":
    main()
