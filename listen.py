import serial
import time
import pymavlink
import csv

# Open serial port for communication with flight controller
fc_serial = serial.Serial('/dev/ttyUSB0', baudrate=115200)

# Create mavlink instance
mav = pymavlink.mavutil.mavlink_connection(fc_serial)

# Wait for the first heartbeat message from the flight controller
mav.wait_heartbeat()

# Open CSV file for writing
csv_file = open('status_messages.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

while True:
    # Wait for STATUSTEXT message
    message = mav.recv_match(type='STATUSTEXT')

    # Print message and save to CSV file
    if message is not None:
        print(message.text)
        csv_writer.writerow([message.text])

    # Wait before checking for next message
    time.sleep(1)

# Close CSV file
csv_file.close()
