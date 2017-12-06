import subprocess
import logging
import re
import pytz
import sys
from datetime import datetime
from awscommon import Common

NAMESPACE = "SSL/ExpireDate"
DOMAINS = ["example.com"]

# get expire date
def get_expire_date(certificate_date):
    now = pytz.timezone('Asia/Tokyo').localize(datetime.now())
    deleta_date = certificate_date - now
    return deleta_date
    

# get certificat date
def get_certificate_date(domain):
    command = "openssl s_client -connect %s:443 -servername %s < /dev/null 2> /dev/null " \
              "| openssl x509 -text | grep 'Not After'" % (domain, domain)

    try:
        output = subprocess.check_output(command, shell=True)
    except Exception as e:
        print "type: %s, domain: %s" % (str(type(e)), domain)
        sys.exit(1)

    date = re.search(r"Not After : (.+)", output)
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    return tokyo_timezone.fromutc(datetime.strptime(
        date.group(1),
        '%b %d %H:%M:%S %Y %Z'))


def main():
    for domain in DOMAINS:
        certificate_date = get_certificate_date(domain)
        expire_date = get_expire_date(certificate_date)
    
        common = Common()
        common.cw_put_metric(NAMESPACE, "ssl_expire_date", expire_date.days, "domain", domain)

    
# main
if __name__ == '__main__':
    main()
