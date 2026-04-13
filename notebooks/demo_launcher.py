import os
import subprocess

import ipywidgets as widgets
from IPython.display import Markdown, display


ROBOTS = ("pr2", "hsrb", "stretch", "tiago")
ENVIRONMENTS = ("apartment", "kitchen", "small_apartment")
TASKS = ("navigate", "pick_up", "transport")

ENV_KEY_MAP = {
    "robot": "NBPARAM_ROBOT",
    "environment": "NBPARAM_ENVIRONMENT",
    "task": "NBPARAM_TASK",
}


def _persist_selection(selection):
    for key, value in selection.items():
        os.environ[ENV_KEY_MAP[key]] = value


def _set_ros_params(node_name, selection):
    results = []
    for key, value in selection.items():
        command = ["ros2", "param", "set", node_name, key, value]
        completed = subprocess.run(command, capture_output=True, text=True)
        results.append(
            {
                "command": " ".join(command),
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    return results


def show_demo_launcher(default_node_name="/demo_launcher"):
    title = widgets.HTML(
        value="""
        <h2 style="margin: 0 0 8px;">Demo Setup</h2>
        <p style="margin: 0 0 14px;">
          Select the robot, environment and task, then set them on a ROS 2 node.
        </p>
        """
    )

    node_name = widgets.Text(
        value=default_node_name,
        description="Node:",
        placeholder="/demo_launcher",
    )
    robot = widgets.Dropdown(options=ROBOTS, value=ROBOTS[0], description="Robot:")
    environment = widgets.Dropdown(
        options=ENVIRONMENTS, value=ENVIRONMENTS[0], description="Env:"
    )
    task = widgets.Dropdown(options=TASKS, value=TASKS[0], description="Task:")
    launch = widgets.Button(
        description="Start Demo",
        button_style="primary",
        icon="play",
    )
    output = widgets.Output()

    controls = widgets.VBox(
        [
            title,
            node_name,
            widgets.HBox([robot, environment, task]),
            launch,
            output,
        ]
    )

    def _on_click(_):
        selection = {
            "robot": robot.value,
            "environment": environment.value,
            "task": task.value,
        }
        selected_node = node_name.value.strip()
        _persist_selection(selection)

        with output:
            output.clear_output(wait=True)
            display(
                Markdown(
                    f"Setting ROS 2 params on `{selected_node}` with "
                    f"`{selection['robot']}`, `{selection['environment']}`, "
                    f"`{selection['task']}`."
                )
            )
            print("Selected values:", selection)
            print(
                "Environment variables:",
                {env_key: os.environ[env_key] for env_key in ENV_KEY_MAP.values()},
            )
            if not selected_node:
                print("ROS 2 node name is empty. Params were not set.")
                return

            results = _set_ros_params(selected_node, selection)
            print("ROS 2 param updates:")
            for result in results:
                print(result["command"])
                if result["stdout"]:
                    print(result["stdout"])
                if result["stderr"]:
                    print(result["stderr"])
                if result["returncode"] != 0:
                    print(f"Command failed with exit code {result['returncode']}")

    launch.on_click(_on_click)
    display(controls)
