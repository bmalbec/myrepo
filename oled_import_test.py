from US2066 import US2066Base as DISP

disp = DISP(0x3C)

disp.begin()

time.sleep(0.01)

disp.command(0x01)
time.sleep(0.001)
disp.write("Hello World!!")
