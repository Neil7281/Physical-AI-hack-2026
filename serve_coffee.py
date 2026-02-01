import pexpect
import sys

def run_inference():
    child = pexpect.spawn(
        'python solo.py',
        encoding='utf-8',
        timeout=20
    )

    child.logfile = sys.stdout

    child.expect('Would you like to use these preconfigured Infence settings')
    child.sendline('n')

    child.expect('Would you like to teleoperation during inference')
    child.sendline('n')

    child.expect('Enter follower id')
    child.sendline('n')

    child.expect('Duration of inference session in seconds')
    child.sendline('60')

    child.expect('Enter viewing angle for Camera #0')
    child.sendline('wrist')

    child.expect('Enter viewing angle for Camera #1')
    child.sendline('top')

    child.expect('Select cameras')
    child.sendline('0,1')

    child.expect(pexpect.EOF)


if __name__ == "__main__":
    run_inference()
    run_inference()
    run_inference()