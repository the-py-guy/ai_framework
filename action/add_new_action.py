import argparse, json, random, string, base64

def create_action(trigger):
	f_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	with open('intents/'+f_name+'.json','w') as f:
		data = {}
		data['intents'] = []
		data['intents'].append({'tag':f_name,'patterns':[trigger],'responses':['$action:'+f_name+'.py'],'context_set':""})
		json.dump(data, f)
	with open('action/'+f_name+'.py','a') as f:
		f.write('# saying: "'+trigger+'" will execute this script.\n')
		template = open('action/templates/action_template.py','r')
		for line in template.readlines():
			f.write(line)
		template.close()

def main(data):
	while True:
		trigger = input('what action should i add?')
		create_action(trigger)

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True)
args = parser.parse_args()
wrapped = args.data
unwrapped = base64.b64decode(wrapped.encode('utf-8'))
call_json = json.loads(unwrapped.decode('utf-8'))
main(call_json)