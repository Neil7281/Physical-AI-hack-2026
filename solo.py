from rich.prompt import Prompt
from time import sleep

Prompt.ask("Would you like to use these preconfigured Infence settings? [y/n]", default="y")
sleep(1)

Prompt.ask("Would you like to teleoperation during inference? [y/n]", default="n")
sleep(2)

Prompt.ask("Enter follower id", default="1")
sleep(1)

Prompt.ask("Duration of inference session in seconds", default="60")
sleep(2)

Prompt.ask("Enter viewing angle for Camera #0 (OpenCV - ID: /dev/video0)", default="front")
sleep(2)

Prompt.ask("Enter viewing angle for Camera #1 (OpenCV - ID: /dev/video2)", default="front")
sleep(1)

Prompt.ask("Select cameras", default="0")
sleep(1)