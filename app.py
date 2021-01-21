# -*- coding: utf-8 -*-


from pprint import pprint
from datetime import datetime
import os
import time
import subprocess

import RPi.GPIO as GPIO
from goprocam import GoProCamera

import click
import requests


OPERATION_LED = 21
STATUS_LED = 26
UPLOAD_LED = 6
NETWORK_ACCESS_LED = 13
GOPRO_WIFI_LED = 5
GOPRO_POWER_LED = 1
GOPRO_OPERATION_LED = 0

GOPRO_POWER_SW = 7

GOPRO_HOST = 'http://10.5.5.9/gp/gpControl'
GOPRO_SUPER_CHARGE_DELAY = 1


def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GOPRO_OPERATION_LED, GPIO.OUT)
    GPIO.setup(GOPRO_POWER_LED, GPIO.OUT)
    GPIO.setup(GOPRO_WIFI_LED, GPIO.OUT)
    GPIO.setup(OPERATION_LED, GPIO.OUT)
    GPIO.setup(STATUS_LED, GPIO.OUT)
    GPIO.setup(UPLOAD_LED, GPIO.OUT)
    GPIO.setup(NETWORK_ACCESS_LED, GPIO.OUT)
    GPIO.setup(GOPRO_POWER_SW, GPIO.OUT)


@click.group()
@click.option('--on', '-o', is_flag=True, help='Device ON')
@click.option('--delay', '-d', default=0.2, show_default=True, help='Delay seconds')
@click.option('--car-name', '-n', default=None, show_default=True, help='Car name')
@click.option('--api-url', '-u', default=None, show_default=True, help='API url')
@click.option('--auth-client-id', '-i', default=None, show_default=True, help='X-Authorization-Client-Id')
@click.option('--auth-client-secret', '-s', default=None, show_default=True, help='X-Authorization-Client-Secret')
def cli(on, delay, car_name, api_url, auth_client_id, auth_client_secret):
    global g_on, g_delay, g_car_name, g_api_url, g_auth_client_id, g_auth_client_secret
    g_on = on
    g_delay = delay
    g_car_name = car_name
    g_api_url = api_url
    g_auth_client_id = auth_client_id
    g_auth_client_secret = auth_client_secret
    init_gpio()


@cli.command(help='Clean up gpio')
def clean():
    GPIO.cleanup()


@cli.command(help='Test gopro')
def test_gopro():
    try:
        print('Start to test gopro')
        while True:
            GPIO.output(GOPRO_OPERATION_LED, GPIO.LOW)
            GPIO.output(GOPRO_POWER_LED, GPIO.LOW)
            GPIO.output(GOPRO_WIFI_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(GOPRO_OPERATION_LED, GPIO.HIGH)
            GPIO.output(GOPRO_POWER_LED, GPIO.HIGH)
            GPIO.output(GOPRO_WIFI_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Finish to test gopro')


@cli.command(help='Test action cam I/F board')
def test_board():
    try:
        print('Start to test action cam I/F board')
        while True:
            GPIO.output(OPERATION_LED, GPIO.LOW)
            GPIO.output(STATUS_LED, GPIO.LOW)
            GPIO.output(UPLOAD_LED, GPIO.LOW)
            GPIO.output(NETWORK_ACCESS_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(OPERATION_LED, GPIO.HIGH)
            GPIO.output(STATUS_LED, GPIO.HIGH)
            GPIO.output(UPLOAD_LED, GPIO.HIGH)
            GPIO.output(NETWORK_ACCESS_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Finish to test action cam I/F board')


@cli.command(help='Power switch on GOPRO')
def gopro_power_sw():
    if g_on:
        GPIO.output(GOPRO_POWER_SW, GPIO.HIGH)
        GPIO.output(GOPRO_POWER_LED, GPIO.HIGH)
    else:
        GPIO.output(GOPRO_POWER_SW, GPIO.LOW)
        GPIO.output(GOPRO_POWER_LED, GPIO.LOW)


@cli.command(help='Power LED on GOPRO')
def gopro_power_led():
    if g_on:
        GPIO.output(GOPRO_POWER_LED, GPIO.HIGH)
    else:
        GPIO.output(GOPRO_POWER_LED, GPIO.LOW)


@cli.command(help='Operation LED on GOPRO')
def gopro_operation_led():
    if g_on:
        GPIO.output(GOPRO_OPERATION_LED, GPIO.HIGH)
    else:
        GPIO.output(GOPRO_OPERATION_LED, GPIO.LOW)


@cli.command(help='Wifi LED on GOPRO')
def gopro_wifi_led():
    if g_on:
        GPIO.output(GOPRO_WIFI_LED, GPIO.HIGH)
    else:
        GPIO.output(GOPRO_WIFI_LED, GPIO.LOW)


@cli.command(help='Operation LED')
def operation_led():
    if g_on:
        GPIO.output(OPERATION_LED, GPIO.HIGH)
    else:
        GPIO.output(OPERATION_LED, GPIO.LOW)


@cli.command(help='Operation LED')
def operation_led_blink():
    try:
        print('Blink operation LED')
        while True:
            GPIO.output(OPERATION_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(OPERATION_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Blink OFF')


@cli.command(help='Status LED')
def status_led():
    if g_on:
        GPIO.output(STATUS_LED, GPIO.HIGH)
    else:
        GPIO.output(STATUS_LED, GPIO.LOW)


@cli.command(help='Blink status LED')
def status_led_blink():
    try:
        print('Blink status LED')
        while True:
            GPIO.output(STATUS_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(STATUS_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Blink OFF')


@cli.command(help='Upload LED')
def upload_led():
    if g_on:
        GPIO.output(UPLOAD_LED, GPIO.HIGH)
    else:
        GPIO.output(UPLOAD_LED, GPIO.LOW)


@cli.command(help='Blink upload LED')
def upload_led_blink():
    try:
        print('Blink upload LED')
        while True:
            GPIO.output(UPLOAD_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(UPLOAD_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Blink OFF')


@cli.command(help='Network access LED')
def network_access_led():
    if g_on:
        GPIO.output(NETWORK_ACCESS_LED, GPIO.HIGH)
    else:
        GPIO.output(NETWORK_ACCESS_LED, GPIO.LOW)


@cli.command(help='Blink network access LED')
def network_access_led_blink():
    try:
        print('Blink network access LED')
        while True:
            GPIO.output(NETWORK_ACCESS_LED, GPIO.LOW)
            time.sleep(g_delay)
            GPIO.output(NETWORK_ACCESS_LED, GPIO.HIGH)
            time.sleep(g_delay)
    except KeyboardInterrupt:
        pass
    finally:
        print('Blink OFF')


@cli.command(help='Sleep GOPRO ')
def gopro_sleep():
    gp = GoProCamera.GoPro()
    gp.power_off()
    GPIO.output(GOPRO_OPERATION_LED, GPIO.LOW)


@cli.command(help='Wake up GOPRO ')
def gopro_wakeup():
    gp = GoProCamera.GoPro()
    ap_mac = '06416989c8c4'
    gp.power_on(ap_mac)
    GPIO.output(GOPRO_OPERATION_LED, GPIO.HIGH)


@cli.command(help='Information of GOPRO ')
def gopro_info():
    gp = GoProCamera.GoPro()
    info = gp.infoCamera()
    pprint(info)    


@cli.command(help='Overview of GOPRO ')
def gopro_overview():
    gp = GoProCamera.GoPro()
    overview = gp.overview()
    pprint(overview)    


@cli.command(help='gpControl of GOPRO ')
def gopro_gpcontrol():
    res = requests.get(GOPRO_HOST, timeout=5)
    pprint(res.json())


@cli.command(help='Status of GOPRO ')
def gopro_status():
    res = requests.get('{}/status'.format(GOPRO_HOST), timeout=5)
    status = res.json()['status']
    doc = {
        'internal_battery_present': status['1'],
        'internal_battery_level': status['2'],
        'internal_battery_percentage': status['70'],
        'system_hot': status['6'],
        'system_busy': status['8'],
        'system_ready': status['82']
    }
    pprint(doc)


@cli.command(help='Live stream of GOPRO ')
def gopro_live_stream():
    res = requests.get('{}/execute?p1=gpStream&a1=proto_v2&c1=restart'.format(GOPRO_HOST), timeout=5)
    pprint(res.json())


@cli.command(help='Power switch reset on GOPRO')
def gopro_power_sw_reset():
    GPIO.output(GOPRO_POWER_SW, GPIO.LOW)
    time.sleep(g_delay)
    GPIO.output(GOPRO_POWER_SW, GPIO.HIGH)


@cli.command(help='Super charge on GOPRO')
def gopro_super_charge():
    GPIO.output(GOPRO_POWER_SW, GPIO.LOW)
    time.sleep(GOPRO_SUPER_CHARGE_DELAY)
    GPIO.output(GOPRO_POWER_SW, GPIO.HIGH)


@cli.command(help='Start video on B101 (Experimental)')
def b101_start():
    cmd_list = ['/usr/bin/v4l2-ctl', '--set-edid=file=/usr/bin/1080P50EDID.txt', '--fix-edid-checksums']
    proc_1= subprocess.Popen(cmd_list)
    pprint(proc_1.pid)
    time.sleep(2)
    cmd_list = ['/usr/bin/yavta.250', '--capture=2147483647', '-n', '3', '--encode-to=-', '-s', '1920x1080', '-f', 'UYVY', '-m', '-T', '/dev/video0', '|', '/usr/bin/gst-launch-1.0', 'fdsrc', 'num-buffers=-1', '!', 'video/x-h264,width=1920,height=1080,framerate=30/1', '!', 'h264parse', '!', 'mpegtsmux', '!', 'filesink', 'location=./test20201118.mp4']
    proc_2= subprocess.Popen(cmd_list)
    pprint(proc_2.pid)
    cmd_list = ['/usr/bin/vlc', '-vvv', 'alsa://hw1,0', '--sout', '"#transcod{acodec=mp3,ab=128,channels=2,samplerate=48000}:std{access=file,mux=raw,dst=test20201118.mp4}"']
    proc_3= subprocess.Popen(cmd_list)
    pprint(proc_3.pid)
    time.sleep(10)
    proc_2.terminate()
    proc_3.terminate()
    cmd_list = ['/usr/bin/v4l2-ctl', '--clear-edid']
    proc_4= subprocess.Popen(cmd_list)
    pprint(proc_4.pid)


@cli.command(help='Upload log file of actioncam app')
def actioncam_log_upload():
    print('start to analyze log file')
    now = datetime.now()
    today = now.strftime('%Y%m%d%H%M%S')
    write_file = '/home/pi/gopro/{}.txt'.format(today)
    wfp = open(write_file, 'w')
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    read_file = '/var/log/syslog'
    with open(read_file, 'r') as fp:
        for l in fp.readlines():
            dt = l.split('raspberrypi')[0].strip()
            dt = datetime.strptime(dt, '%b %d %H:%M:%S')
            dt = dt.replace(year=now.year)
            if dt >= now:
                wfp.write(l)
    wfp.close()
    print('created analyzed log file: {}'.format(write_file))
    print('start upload file: {}'.format(write_file))
    upload_url = '{}/actioncams/{}/log/files'.format(g_api_url, g_car_name)
    headers = {
        'X-Authorization-Client-Id': g_auth_client_id,
        'X-Authorization-Client-Secret': g_auth_client_secret
    }
    files = [
        ('file', ('{}.txt'.format(today), open(write_file, 'rb'), 'text/plain'))
    ]
    res = requests.post(upload_url, headers=headers, files=files)
    print('status code is {}'.format(res.status_code))
    if res.status_code == 200:
        os.remove(write_file)
    print('finish upload file')


if __name__ == '__main__':
    cli()

