from urllib.request import urlopen
import json
import os
from datetime import datetime

os.chdir("/home/debian/Scripts/mikrotik_aws_iplist");

url = "https://ip-ranges.amazonaws.com/ip-ranges.json";
data = json.loads(urlopen(url).read().decode("utf-8"));
generationDate = "{} CET".format(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"));

ipv4_regions = set([entry["region"] for entry in data["prefixes"]]);

with open("./aws_ipv4_all.rsc","w") as f_all:
	f_all.write("# Generated on {}\n".format(generationDate));
	f_all.write("/ip firewall address-list\n");
	for region in ipv4_regions:
		prefixFiltered = [prefix for prefix in data["prefixes"] if prefix["region"] == region];
		with open("./regions/ipv4_{}.rsc".format(region), "w") as f_svc:
			f_svc.write("# Generated on {}\n".format(generationDate));
			f_svc.write("/ip firewall address-list\n");
			for prefix in prefixFiltered:
				f_svc.write("add list=aws_{} address={}\n".format(prefix["region"],prefix["ip_prefix"]));
				f_all.write("add list={} address={}\n".format("aws_ipv4_all",prefix["ip_prefix"]));


ipv6_regions = set([entry["region"] for entry in data["ipv6_prefixes"]]);

with open("./aws_ipv6_all.rsc","w") as f_all:
        f_all.write("# Generated on {}\n".format(generationDate));
        f_all.write("/ipv6 firewall address-list\n");
        for region in ipv6_regions:
                prefixFiltered = [prefix for prefix in data["ipv6_prefixes"] if prefix["region"] == region];
                with open("./regions/ipv6_{}.rsc".format(region), "w") as f_svc:
                        f_svc.write("# Generated on {}\n".format(generationDate));
                        f_svc.write("/ipv6 firewall address-list\n");
                        for prefix in prefixFiltered:
                                f_svc.write("add list=aws_{}_v6 address={}\n".format(prefix["region"],prefix["ipv6_prefix"]));
                                f_all.write("add list={} address={}\n".format("aws_ipv6_all",prefix["ipv6_prefix"]));

os.system('git add .');
os.system('git commit -m "{} - Amader - uploaded converted AWS ip range files for Mikrotik"'.format(datetime.now().strftime("%Y-%m-%d")));
os.system('git push origin main');
