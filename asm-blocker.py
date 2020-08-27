import requests
import argparse


#Specify ASM Domain or IP
asmaddress = "CHANGEME"

#Specify username:password in base64
auth = "CHANGEME"


parser = argparse.ArgumentParser(description='F5 ASM IP Address Blocker')

parser.add_argument('-a', '--address', help='IP Address', required=True)
parser.add_argument('-p', '--policy', help='Policy Full path. Example: /Common/website.ge_policy', required=True)
parser.add_argument('-o', '--operation', choices=['block', 'unblock'], help='Type operation. Allowed values are: block OR unblock', required=True)
args = parser.parse_args()

asmauth = "Basic " + auth


def getPolicyId(fullPath):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/policies?$select=id&$filter=name eq '" + fullPath + "'"
	headers = {"Authorization": asmauth}
	r = requests.get(asmurl, verify=False, headers=headers)
	js = r.json()
	return js['items'][0]['id']


def blockIp(ip, id):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/policies/" + id + "/whitelist-ips"
	payload = {"blockRequests": "always", "description": "Blocked By API Client", "ipAddress": ip, "ipMask": "255.255.255.255", "neverLearnRequests": "true"}
	headers = {"Content-Type": "application/json", "Authorization": asmauth}
	requests.post(asmurl, verify=False, headers=headers, json=payload)


def unBlockIp(ip,id):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/policies/" + id + "/whitelist-ips?$filter=ipAddress eq '" + ip + "'"
	headers = {"Authorization": asmauth}
	requests.delete(asmurl, verify=False, headers=headers)


def applyPolicy(id):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/tasks/apply-policy"
	policyurl = "https://localhost/mgmt/tm/asm/policies/" + id
	payload = { "policyReference": { "link" : policyurl } }
	headers = {"Content-Type": "application/json", "Authorization": asmauth}
	r = requests.post(asmurl, verify=False, headers=headers, json=payload)



if args.operation == "block":
	blockIp(args.address, getPolicyId(args.policy))
	applyPolicy(getPolicyId(args.policy))
if args.operation == "unblock":
	unBlockIp(args.address, getPolicyId(args.policy))
	applyPolicy(getPolicyId(args.policy))
