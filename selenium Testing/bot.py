# Import for integration with BotCity Maestro SDK
from botcity.maestro import (  # noqa: E402
    BotMaestroSDK,
    AlertType,
    AutomationTaskFinishStatus,
)

from quick_demo import main as quick_demo_main  # noqa: E402
# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")  # noqa: T201
    print(f"Task Parameters are: {execution.parameters}")  # noqa: T201
    print("starting...")
    print("starting... done...")
    maestro.alert(task_id=execution.task_id, title="Example Bot started!", message="The bot has started its execution.", alert_type=AlertType.INFO)

    # Here you can call your main.py file or implement your bot's logic
    quick_demo_main()
    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Congratulations on finishing first task with success. 🎉",
        
    )

if __name__ == "__main__":
    main()
