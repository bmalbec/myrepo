import US2066

disp = US2066Base(0x3C)

disp.begin()

time.sleep(0.01)

disp.command(0x01)
time.sleep(0.001)
disp.write("Hello World!")
