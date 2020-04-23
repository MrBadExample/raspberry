import subprocess
import config
from influxdb import InfluxDBClient


speed_test_response = subprocess.Popen('df -l',
                                       shell=True,
                                       stdout=subprocess.PIPE).stdout.read().decode('utf-8')


def append_values_to_influxdb():
    for line in speed_test_response.splitlines():
        if not (line.startswith('tmpfs') or line.startswith('Filesystem') or line.startswith('devtmpfs')):
            values = line.split()
            filesystem = values[0].split('/')[2]
            size = values[1]
            used = values[2]
            available = values[3]
            # used_perc = str(values[4])
            # mounted = str(values[5])

            disk_usage_data = [
                {
                    "measurement": filesystem,
                    "tags": {
                        "host": 'homeserver'
                    },
                    "fields": {
                        "size": float(size),
                        "used": float(used),
                        "available": float(available),
                        # "used_perc": used_perc,
                        # "mounted": mounted,
                    }
                }
            ]

            client = InfluxDBClient(config.ip,
                                    config.port,
                                    config.user,
                                    config.password,
                                    config.disk_usage_database)

            client.write_points(disk_usage_data)


append_values_to_influxdb()