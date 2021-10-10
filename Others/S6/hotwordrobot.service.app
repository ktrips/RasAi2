Description=Hotword Robot
[Service]
ExecStart=/bin/bash /home/pi/Programs/hotword_robot.sh
WorkingDirectory=/home/pi/Programs/
Restart=always
User=pi
[Install]
WantedBy=multi-user.target

