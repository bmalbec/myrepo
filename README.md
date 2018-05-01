# capstone-files
This is the Github repository for the [NT]<sup>2</sup> ESET 420 Capstone Project

Welcome!  :trident:

## Controller 
The following sections contain instructions to set up the controller side of the capstone project.

### Resources Needed
- Ubuntu for BeagleBone
- ROS Kinetic
- Python 2.7 or newer
- Xbox 360 Controller

### Installation
1. Using an 8GB microSD card, install Ubuntu 16.04 designed for [BeagleBone](https://elinux.org/BeagleBoardUbuntu#Method_1:_Download_a_Complete_Pre-Configured_Image)
2. Log in to the BeagleBone using the default credentials
   - Username: ubuntu
   - Password: temppwd
3. [Establish an internet connection](https://www.digikey.com/en/maker/blogs/how-to-connect-a-beaglebone-black-to-the-internet-using-usb)
4. Link [this respository](https://github.com/tamucapstone/capstone-files) to the home directory ([Tutorial](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/))
5. [Install ROS Kinetic (Bare Bones, not desktop or "full")](http://wiki.ros.org/kinetic/Installation/Ubuntu)
6. Follow the [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials) for installing catkin and beginner_tutorials
7. Install and configure the ROS [joy](http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick) package
8. Make the Python script "Controller_headless.py" executable:
```
chmod +x Controller_headless.py
```
9. In the /home/ubuntu/catkin_ws/src/beginner_tutorials directory, add two directories called "scripts" and "launch":
```
mkdir scripts
mkdir launch
```
10. Place "Controller_headless.py" and "US2066.py" in the "scripts" directory, and "launchjoy.launch" in the "launch" directory:
```
cd <location of the Python files>
cp Controller_headless.py US2066.py ~/catkin_ws/src/beginner_tutorials/scripts
cp launchjoy.launch ~/catkin_ws/src/beginner_tutorials/launch
```
11. Go back to the home directory, then create the boot .service file in the boot directory:
```
cd
sudo nano /etc/systemd/system/(boot_filename).service
```
12. Use the following criteria for the .service file:
```
[Unit]
Description = [NT]^2 controller boot script
After = mysql.service
[Service]
ExecStart = /usr/local/bin/(bash_filename).sh
[Install]
WantedBy = default.target
```
13. Create the following bash script in the /usr/local/bin directory:
```
cd
sudo nano /usr/local/bin/(bash_filename).sh
```
14. Use the following criteria for the bash .sh file:
```
#!/usr/bin/env bash
bash -c "source /home/ubuntu/catkin_ws/devel/setup.bash && roslaunch beginner_tutorials launchjoy.launch"
```
15. Make the bash .sh file executable:
```
chmod +x /usr/local/bin/(bash_filename).sh
```
16. Test for functionality:
```
systemctl start Controller_Boot.service
systemctl status Controller_Boot.service
```

##  ROV
The following sections contain instructions to set up the ROV side of the capstone project.

### Resources Needed
- Ubuntu for BeagleBone
- Python 2.7 or newer
- PCA 9685 Python library
### Installation
1. Using an 8GB microSD card, install Ubuntu 16.04 designed for [BeagleBone](https://elinux.org/BeagleBoardUbuntu#Method_1:_Download_a_Complete_Pre-Configured_Image)
2. Log in to the BeagleBone using the default credentials
   - Username: ubuntu
   - Password: temppwd
3. [Establish an internet connection](https://www.digikey.com/en/maker/blogs/how-to-connect-a-beaglebone-black-to-the-internet-using-usb)
4. Link [this respository](https://github.com/tamucapstone/capstone-files) to the home directory ([Tutorial](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/))
5. Install the Python library for the [PCA 9685 Hardware PWM](https://github.com/adafruit/Adafruit_Python_PCA9685)
6. Make the Python script "rov_april_9.py" executable:
```
chmod +x rov_april_9.py
```
7. Create the boot .service file in the boot directory:
```
cd
sudo nano /etc/systemd/system/(boot_filename).service
```
8. Use the following criteria for the .service file:
```
[Unit]
Description = [NT]^2 ROV boot script
After = mysql.service
Restart = always
[Service]
ExecStart = /usr/local/bin/(bash_filename).sh
[Install]
WantedBy = default.target
```
9. Create the following bash script in the /usr/local/bin directory:
```
cd
sudo nano /usr/local/bin/(bash_filename).sh
```
10. Use the following criteria for the bash .sh file:
```
#!/usr/bin/env bash
bash -c "/home/ubuntu/rov_bash.sh"
```
11. Make the bash .sh file executable:
```
chmod +x /usr/local/bin/(bash_filename).sh
```
12. In the home directory, make rov_bash.sh executable:
```
cd
chmod +x rov_bash.sh
```
