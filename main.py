import vcf

def import_contacts_from_file(file):
	with open('files/' + file,'r') as f:
		raw = f.read();
	# split contents of file by newline
	split = raw.split('\n')
	return split

def separate_vcf_contacts(split):
	# take list of contacts split by newline (\n) and return list of lists
	all_contacts = []
	for line in split:
		# split each entry by mandatory beginning and ending identifiers
		if line.startswith('BEGIN'):
			single_contact = []
		elif line.startswith('END'):
			all_contacts.append(single_contact)
		else:
			single_contact.append(line)
	return all_contacts

def parse_all_vcf_contacts(contacts):
	# global scope function for parsing vCard entries
	master = []
	for x in contacts:
		c = vcf.contact()
		c.extract_vcf(x)
		#c.display_contact()
		master.append(c)
	return master

def parse_all_csv_contacts(contacts):
	master = []
	for x in contacts:
		c = vcf.contact()
		c.extract_csv(x)
		master.append(c)
	return master

def find_name(name,lst,display_item):
	# list comprehension that searches for a matching substring in FN
	results = [contact.__dict__ for contact in lst if name.lower() in contact.info['FN'].lower() ]
	if type(display_item) == str:
		for contact in results: print 'FN:\t{0}\n{1}:\t{2}\n'.format(contact['info']['FN'],display_item.upper(),contact['info'][display_item.upper()])
	elif type(display_item) == list or type(display_item) == tuple:
		for contact in results:
			print '\nFN:\t{0}'.format(contact['info']['FN'])
			for di in display_item:
				try:
					print '{0}:\t{1}'.format(di.upper(),contact['info'][di.upper()])
				except KeyError:
					print '{0}:\tinvalid key'.format(di.upper())
	else:
		print 'cannot display {0}'.format(type(display_item))
	return
	
def find_num(num,lst):
	results = []
	for contact in lst:
		# check for single-entry TEL, as str type
		if type(contact.info['TEL']) is str:
			# extract only numeric values from str for comparison
			pure = filter(str.isdigit, contact.info['TEL'])
			if num in pure: results.append(contact.__dict__)
		# check for multiple-entry TEL, as list type
		elif type(contact.info['TEL']) is list:
			# extract only numeric values from str for comparison
			check = [ contact.__dict__ for y in contact.info['TEL'] if num in filter(str.isdigit, y) ]
			if len(check) > 0: results.extend(check)
	
	for c in results: print 'FN:\t{0}\nTEL:\t{1}\n'.format(c['info']['FN'],c['info']['TEL'])
	return

if __name__ == '__main__':
	# import from vcf first
	imported_contacts = import_contacts_from_file('Contacts.vcf')
	contacts = separate_vcf_contacts(imported_contacts)
	master_list = parse_all_vcf_contacts(contacts)
	# import from test csv
	imported_contacts = import_contacts_from_file('wip.csv')
	master_list.extend(parse_all_csv_contacts(imported_contacts))
