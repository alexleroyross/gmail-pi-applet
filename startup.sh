# /etc/init.d/startup.sh
### BEGIN INIT INFO
# Provides:          startup.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start gmail pi app on boot
# Description:       Start gmail pi app on boot
### END INIT INFO

python3 /home/pi/gmail-pi-applet/main.py