import pexpect
import sys
import signal
import select
from time import sleep

def run_inference(policy, time):
    time = str(time)
    child = pexpect.spawn(
        'solo robo --inference',
        encoding='utf-8',
        timeout=20
    )

    child.logfile = sys.stdout

    child.expect('Would you like to use these preconfigured Inference settings')
    child.sendline('n')

    child.expect('Would you like to teleoperate during inference')
    child.sendline('n')

    child.expect('Enter follower id')
    child.sendline('1')

    child.expect('Enter policy path')
    child.sendline(policy)

    child.expect('Duration of inference session in seconds')
    child.sendline(time)

    child.expect('Enter task description')
    child.sendline('Grasp cup and lift')

    child.expect('Enter viewing angle for Camera #0')
    child.sendline('wrist')

    child.expect('Enter viewing angle for Camera #1')
    child.sendline('top')

    child.expect('Select cameras')
    child.sendline('0,1')

    # child.expect(pexpect.EOF)

    while True:
        if not child.isalive():
            print("\nChild finished normally")
            break

        # Check for user keypress
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            if key.lower() == 'q':
                print("\n'q' pressed — terminating child")
                child.kill(signal.SIGKILL)
                break

        # Drain child output (non-blocking)
        try:
            child.expect(pexpect.EOF, timeout=0.1)
            break
        except pexpect.TIMEOUT:
            pass

    child.close()


if __name__ == "__main__":
    run_inference("Neil7281/Grasp_ACT_1", 20)
    run_inference("Neil7281/Traverse_ACT_2", 120)
    run_inference("Neil7281/putting_back_SOLO_ACT", 30)
