# auto-speedtest
Automatic speedtest for Linux

This little piece of code is meant for making internet speed tests on regular intervals. The script measures ping, download speed and upload speed and saves the results in an InfluxDB database.

## Prequisites
The script needs the following prequisites to work.
### Speedtest-cli

Install with `sudo apt install speedtest-cli`

### InfluxDB

#### Installation
These installation instructions are for Ubuntu 20.04.

Add repository `echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list`

Add key `sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -`

Update `sudo apt update`

Install InfluxDB `sudo apt-get install influxdb`

#### InfluxDB configuration

Enable service `sudo systemctl enable --now influxdb`

Open port on firewall `sudo ufw allow 8086/tcp`

Let's enable user authentication for InfluxDB

Edit the configuration file `sudo nano /etc/influxdb/influxdb.conf`

From the `[html]` section find a line `# auth-enabled = false`. Remove the hash from the beginning and replace the false with true: `auth-enabled = true`.

Press `CTRL+X`, `Y` and `Enter` to save the file.

Restart the service `sudo systemctl restart influxdb`

Open InfluxDB shell `influx`

Add a new user `CREATE USER username WITH PASSWORD 'password' WITH ALL PRIVILEGES`

You now have to use your credentials every time using the InfluxDB shell

Exit the shell `exit`

Open it again with your credentials `influx -username username -password password`

Create a new database `CREATE DATABASE speedtest`

Check that the newly created database exists `SHOW DATABASES`. It should be on the list.

Exit the shell `exit`

### Python
Many Linux distributions like Ubuntu have Python installed out of the box. You need to install InfluxDB library for it.

Make sure pip is installed `sudo apt-get install python3-pip`

Install InfluxDB library `python3 -m pip install influxdb`

## Installation
Download the file to your computer `wget https://raw.githubusercontent.com/kestis/auto-speedtest/main/measure-speed.py`

Edit the contents of the measure-speed.py `sudo nano measure-speed.py`

Set the credentials on this line `client = InfluxDBClient(host='localhost', port=8086, username='user', password='password')`

Set the correct database name on this line `client.switch_database('speedtest')`

Save the file `CTRL+X`, `Y`, `Enter`

Create a cron job to run the script at desired intervals. For example: `*/15 * * * * $(which python3) measure-speed.py >> /dev/null`

## Checking that the  script works

After the script has been executed open the InfluxDB shell with your credentials `influx -username username -password password`

Select the correct database for use `USE speedtest`

View the data `SELECT * FROM "stats"`

## Data visualization
Grafana is a great tool to visualize the data collected by auto-speedtest. It can use InfluxDB as a data source.
