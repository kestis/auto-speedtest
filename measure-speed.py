import os
from influxdb import InfluxDBClient

#Execute speed test with csv output. You might want to set a server to be used.
stream = os.popen('speedtest-cli --server 22669 --csv')
#Read and split the output
output = stream.read()
parts = output.split(',')
#Extract the ping, download speed and upload speed
ping = int(float(parts[5]))
download = int(float(parts[6]))
upload = int(float(parts[7]))

#Connection to InfluxDB
client = InfluxDBClient(host='localhost', port=8086, username='user', password='password')
#Switch to correct database
client.switch_database('speedtest')
#Create the JSON to be inserted
json = {
	"measurement": "stats",
	"fields": {
		"ping": ping,
		"download": download,
		"upload": upload
	}
}
#Create dictionary
data = []
data.append(json)
#Write data to database
client.write_points(data)
