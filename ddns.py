#!/usr/bin/env python3
"""
 * Build By:
 * https://itheo.tech 2021
 * MIT License
 * Script to set your home (or business) IP address via cloudflare dns on A-record domain record
 * Specially used when you do not have a fixed IP address
"""
import sys
import configparser
import logging
import logging.handlers as handlers
import requests

from time import sleep

import CloudFlare

logger = logging.getLogger('ddns')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler('logs/normal.log', when='M', interval=1, backupCount=0)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

errorLogHandler = handlers.RotatingFileHandler('logs/error.log', maxBytes=5000, backupCount=0)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)

class auto_ddns():
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.zone_id = config['CloudFlare']['zone_id']
        self.api_token = config['CloudFlare']['api_token']
        self.ip_address_type = config['CloudFlare']['ip_address_type']
        self.dns_name = config['CloudFlare']['dns_name']

        self.current_ip = None
        self.cloud_flare_ip = None
        self.cf = None
        self.new_dns_record = None
        self.dns_id = None

    def main(self):
        self.current_ip = self.get_ip()

        if not self.current_ip:
            return False

        if not self.connect_cloud_dns():
            return False

        if not self.get_cloud_dns():
            return False

        # If the cloud flare IP and current IP are the same there is nothing to do, Return!
        if (self.cloud_flare_ip is not None and self.cloud_flare_ip == self.current_ip) or self.new_dns_record is None:
            return True

        if not self.set_cloud_dns():
            return False

        return True

    @staticmethod
    def get_ip():
        try:
            result = requests.get('https://checkip.amazonaws.com')
            if(result.status_code == 200):
                return result.text.strip()
            else:
                return False
        except Exception as e:
            logger.error(e)
            return False

    def connect_cloud_dns(self):
        try:
            self.cf = CloudFlare.CloudFlare(token=self.api_token)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            logger.error(f'API connection failed: {e}')
            return False

        return True

    def get_cloud_dns(self):
        try:
            params = {'name':self.dns_name, 'match':'all', 'type':self.ip_address_type}
            dns_records = self.cf.zones.dns_records.get(self.zone_id, params=params)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            logger.error('/zones/dns_records/export %s - %d %s - api call failed' % (self.zone_id, e, e))
            return False

        for dns_record in dns_records:
            try:
                self.cloud_flare_ip = dns_record['content']
                self.new_dns_record = None

                if(self.current_ip != self.cloud_flare_ip):
                    self.dns_id = dns_record['id']

                    self.new_dns_record = {
                    'name':self.dns_name,
                    'type':self.ip_address_type,
                    'content':self.current_ip,
                    'proxied':dns_record['proxied']  }

            except Exception as e:
                logger.error(e)
                return False

        return True

    def set_cloud_dns(self):
        try:
            dns_record = self.cf.zones.dns_records.put(self.zone_id, self.dns_id, data=self.new_dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            logger.error('/zones.dns_records.put %s - %d %s - api call failed' % (self.dns_name, e, e))
            return False

        logger.info('UPDATED: %s %s -> %s' % (self.dns_name, self.cloud_flare_ip, self.current_ip))
        return True


if __name__ == '__main__':
    ddns = auto_ddns()
    while True:
        if ddns.main():
            sleep(900) # 15 minutes
        else:
            # I guess something went wrong, let's give the script a bit more time.
            sleep(1800) # 30 minutes