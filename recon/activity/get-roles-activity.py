#this script will invoke AWS CLI to check if there are unused roles by extracting from IAM a list of:
#role | last used date

#NOTE: it will take the default profile for your AWS CLI.
#it will use creds for log into aws. Skip that part if you cannot use creds
#----------------------------------------------------------------------------------

import subprocess
from datetime import datetime

#Get today date to calculate how many days passed since the last role usage
today = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
today = datetime.strptime(today, "%Y-%m-%dT%H:%M:%SZ")

#list of accounts and the role to use
accounts = ["ACCOUNT_ONE","ACCOUNT_TWO"]
account_role = "ROLENAME"
cmd_rlist = 'aws iam list-roles | jq ".Roles[].RoleName"'

#Loop in all accounts with tf-ops-role (not everyone has readonly role)
for account in accounts:
	try:
		cmd = "creds aws login "+account+" "+account_role
	except Exception as e:
		print (e)
		continue

	#GET ROLES LIST
	p = subprocess.Popen(cmd_rlist, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	roles = output.split()

	for role in roles:
		#GET ROLE LAST USED DATE
		role = role.replace('"','')
		cmd_rlu = 'aws iam get-role --role-name '+role+' | jq ".Role.RoleLastUsed.LastUsedDate"'
		p = subprocess.Popen(cmd_rlu, stdout=subprocess.PIPE, shell=True)
		(lastused, err) = p.communicate()
		lastused = lastused.replace('"','').replace("\n","")
		try:
			d1 = datetime.strptime(lastused, "%Y-%m-%dT%H:%M:%SZ")
			days = ((today - d1).days)
		except:
			days = "null"

		#PRINT ROLE-LAST USED
		print("%s,%s,%s,%s" %(account,role,lastused,days))
