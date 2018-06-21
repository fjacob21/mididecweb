import datetime
from ua_parser import user_agent_parser
import requests

class LogGenerator(object):

    def __init__(self, ip, user_agent):
        self._ip = ip
        self._user_agent = user_agent

    def generate(self):
        useragent = self.parse_user_agent()
        geoinfo = self.fetch_geo_info()
        log = {}
        log['ip'] = self._ip
        log['is_eu'] = geoinfo['is_eu']
        log['os'] = useragent['os']
        log['os_version'] = useragent['os_version']
        log['browser'] = useragent['browser']
        log['browser_version'] = useragent['browser_version']
        log['region'] = geoinfo['region']
        log['city'] = geoinfo['city']
        log['country'] = geoinfo['country']
        log['continent'] = geoinfo['continent']
        log['country_emoji'] = geoinfo['country_emoji']
        log['date'] = datetime.datetime.now().isoformat()
        return log

    def parse_user_agent(self):
        useragent = self.default_user_agent()
        parsed = user_agent_parser.Parse(self._user_agent)
        if 'os' in parsed:
            os = parsed['os']
            if 'family' in os:
                useragent['os'] = os['family']
            os_version_major = '0'
            if 'major' in os and os['major']:
                os_version_major = os['major']
            os_version_minor = '0'
            if 'minor' in os and os['minor']:
                os_version_minor = os['minor']
            os_version_patch = '0'
            if 'patch' in os and os['patch']:
                os_version_patch = os['patch']
            useragent['os_version'] = os_version_major + '.' + os_version_minor + '.' + os_version_patch
        if 'user_agent' in parsed:
            user_agent = parsed['user_agent']
            if 'family' in user_agent:
                useragent['browser'] = user_agent['family']
            browser_version_major = '0'
            if 'major' in user_agent and user_agent['major']:
                browser_version_major = user_agent['major']
            browser_version_minor = '0'
            if 'minor' in user_agent and user_agent['minor']:
                browser_version_minor = user_agent['minor']
            browser_version_patch = '0'
            if 'patch' in user_agent and user_agent['patch']:
                browser_version_patch = user_agent['patch']
            useragent['browser_version'] = browser_version_major + '.' + browser_version_minor + '.' + browser_version_patch
        return useragent

    def default_user_agent(self):
        useragent = {}
        useragent['os'] = ''
        useragent['os_version'] = '0.0.0'
        useragent['browser'] = ''
        useragent['browser_version'] = '0.0.0'
        return useragent

    def fetch_geo_info(self):
        geoinfo = self.default_geo_info()
        try:
            url = 'http://api.ipstack.com/'
            url += '{0}?'.format(self._ip)
            url += 'access_key=98e04078598f19c362b9dfa2405885fe'
            reply = requests.get(url)
            if reply.ok:
                geoinfo_dict = reply.json()
                if 'location' in geoinfo_dict:
                    location = geoinfo_dict['location']
                    if 'is_eu' in location:
                        geoinfo['is_eu'] = location['is_eu']
                    if 'country_flag_emoji' in location:
                        geoinfo['country_emoji'] = location['country_flag_emoji']
                if 'region_name' in geoinfo_dict:
                    geoinfo['region'] = geoinfo_dict['region_name']
                if 'city' in geoinfo_dict:
                    geoinfo['city'] = geoinfo_dict['city']
                if 'country_name' in geoinfo_dict:
                    geoinfo['country'] = geoinfo_dict['country_name']
                if 'continent_name' in geoinfo_dict:
                    geoinfo['continent'] = geoinfo_dict['continent_name']
        except:
            pass
        return geoinfo

    def default_geo_info(self):
        geoinfo = {}
        geoinfo['is_eu'] = True
        geoinfo['region'] = ''
        geoinfo['city'] = ''
        geoinfo['country'] = ''
        geoinfo['continent'] = ''
        geoinfo['country_emoji'] = ''
        return geoinfo
