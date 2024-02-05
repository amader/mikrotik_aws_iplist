from urllib.request import urlopen
import json
from datetime import datetime

url = "https://ip-ranges.amazonaws.com/ip-ranges.json";
data = json.loads(urlopen(url).read().decode("utf-8"));
generationDate = "{} CET".format(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"));

ipv4_services = set([(entry["service"], entry["region"]) for entry in data["prefixes"]]);

with open("./lists/aws_ipv4_all.rsc","w") as f_all:
	f_all.write("# Generated on {}\n".format(generationDate));
	f_all.write("/ip firewall address-list\n");
	for service in ipv4_services:
		prefixFiltered = [prefix for prefix in data["prefixes"] if prefix["service"] == service[0] and prefix["region"] == service[1]];
		with open("./lists/services/ipv4_{}_{}.rsc".format(service[0], service[1]), "w") as f_svc:
			f_svc.write("# Generated on {}\n".format(generationDate));
			f_svc.write("/ip firewall address-list\n");
			for prefix in prefixFiltered:
				f_svc.write("add list={}_{} address={}\n".format(prefix["service"],prefix["region"],prefix["ip_prefix"]));
				f_all.write("add list={} address={}\n".format("aws_ipv4_all",prefix["ip_prefix"]));


ipv6_services = set([(entry["service"], entry["region"]) for entry in data["ipv6_prefixes"]]);

with open("./lists/aws_ipv6_all.rsc","w") as f_all:
        f_all.write("# Generated on {}\n".format(generationDate));
        f_all.write("/ipv6 firewall address-list\n");
        for service in ipv6_services:
                prefixFiltered = [prefix for prefix in data["ipv6_prefixes"] if prefix["service"] == service[0] and prefix["region"] == service[1]];
                with open("./lists/services/ipv6_{}_{}.rsc".format(service[0], service[1]), "w") as f_svc:
                        f_svc.write("# Generated on {}\n".format(generationDate));
                        f_svc.write("/ipv6 firewall address-list\n");
                        for prefix in prefixFiltered:
                                f_svc.write("add list={}_{}_v6 address={}\n".format(prefix["service"],prefix["region"],prefix["ipv6_prefix"]));
                                f_all.write("add list={} address={}\n".format("aws_ipv6_all",prefix["ipv6_prefix"]));
