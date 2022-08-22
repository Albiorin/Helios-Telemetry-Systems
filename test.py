import hid

gamepad = hid.device()
gamepad.open(0x046d, 0xc215)
gamepad.set_nonblocking(True)
while True:
    report = gamepad.read(64)
    if report:
        print(report)
    if 1 == 2:
        break