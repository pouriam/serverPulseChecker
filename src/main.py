from configparser import ConfigParser, ExtendedInterpolation
from optparse import OptionParser
import socket
import sys
import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_config_parameters(sys_args):
    config_path = 'config/config.cfg'
    if sys_args:
        config_path = sys_args[0]

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_path, encoding="utf-8")
    return config


def is_int(val):
    try:
        value = int(val)
        return True
    except ValueError:
        return False


def connect_server(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        return True, None
    except Exception as e:
        return False, e
    finally:
        s.close()


def check_server(conf):
    parser = OptionParser()
    while True:
        msg_body = ""
        for section in conf.sections():
            if section != 'general':
                for key in conf[section]:
                    if is_int(conf[section][key]):
                        parser.add_option("-p", "--port", dest="port", type="int", default=conf[section][key], help="Server Port")
                    else:
                        parser.add_option("-a", "--address", dest="address", default=conf[section][key], help="Server Address")
                (options, args) = parser.parse_args()
                parser.remove_option("-p")
                parser.remove_option("-a")
                server_connected, error_message = connect_server(options.address, options.port)
                if not server_connected:
                    d = {'section': section}
                    err_msg = "'{}' is not listening on port '{}' due to: {}".format(options.address, options.port, error_message)
                    msg_body += err_msg + "\n"
                    logger.error(err_msg, extra=d)

        if msg_body:
            send_email(conf, msg_body)

        time.sleep(int(conf['general']['interval']))


def send_email(configuration, message_body):
    s = smtplib.SMTP(host=cfg['general']['smtp.host'], port=configuration['general']['smtp.port'])
    s.starttls()
    s.login(configuration['general']['smtp.login.email'], configuration['general']['smtp.login.password'])

    msg = MIMEMultipart()
    msg['From'] = configuration['general']['from.email']
    msg['To'] = configuration['general']['from.email']
    msg['Subject'] = configuration['general']['email.subject']

    msg.attach(MIMEText(message_body, 'plain'))

    s.send_message(msg)
    del msg
    s.quit()

if __name__ == '__main__':

    cfg = get_config_parameters(sys.argv[1:])
    logging.basicConfig(format=str(cfg['general']['logging.format']))
    logger = logging.getLogger('Server Pulse Checker')

    check_server(cfg)
