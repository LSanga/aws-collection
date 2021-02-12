#this script will invoke AWS CLI to check if there are unused keys by extracting from IAM a list of:
#user | key(s) | last key(s) activity

#NOTE: it will take the default profile for your AWS CLI.
#----------------------------------------------------------------------------------


import subprocess

cmd_ulist = 'aws iam list-users | jq ".Users[].UserName"'

#GET USER LIST
p = subprocess.Popen(cmd_ulist, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
users = output.split()

for user in users:
	#GET USER KEYs
	user = user.replace('"','')
	cmd_uak = 'aws iam list-access-keys --user-name '+user+' | jq ".AccessKeyMetadata[].AccessKeyId"'
	p = subprocess.Popen(cmd_uak, stdout=subprocess.PIPE, shell=True)
	(keys, err) = p.communicate()

	keys = keys.replace('"','').split()
	keys_activity = []
	for key in keys:
		#GET LAST TIME THE KEY WAS USED
		cmd_aklu = 'aws iam get-access-key-last-used --access-key-id '+key+' | jq ".AccessKeyLastUsed.LastUsedDate"'
		c = subprocess.Popen(cmd_aklu, stdout=subprocess.PIPE, shell=True)
		(lastused, err) = c.communicate()
		lastused = lastused.replace('"','').split()
		keys_activity.append(lastused[0])

	#PRINT USER-KEY(s)-ACTIVITY
	print(user,keys,keys_activity)
