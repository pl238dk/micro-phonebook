class contact(object):
	def __init__(self):
		# list majority of known keys according to RFC 6350
		self.info = {
			##'BEGIN':None,
			##'END':None,
			'ADR':None, ## po box; extend adr; street; address; city; region; zip; country
			'AGENT':None,
			'ANNIVERSARY':None,
			'BDAY':None,
			'CALADRURI':None,
			'CALURI':None,
			'CATEGORIES':None,
			'CLASS':None,
			'CLIENTPIDMAP':None,
			'EMAIL':None,
			'FBURL':None,
			'FN':None,
			'GENDER':None,
			'GEO':None,
			'IMPP':None,
			'KEY':None,
			'KIND':None,
			'LABEL':None,
			'LANG':None,
			'LOGO':None,
			'MAILER':None,
			'MEMBER':None,
			'N':None, ## ; Family; Given; Middle; Prefix; Suffix.
			'NAME':None,
			'NICKNAME':None,
			'NOTE':None,
			'ORG':None,
			'PHOTO':None,
			'PRODID':None,
			'PROFILE':None,
			'RELATED':None,
			'REV':None,
			'ROLE':None,
			'SORT-STRING':None,
			'SOUND':None,
			'SOURCE':None,
			'TEL':None,
			'TITLE':None,
			'TZ':None,
			'UID':None,
			'URL':None,
			'VERSION':None,
			'XML':None,
			## Custom
			'X-ABUID':None,
			'X-ANDROID-CUSTOM':None,
			'X-ANNIVERSARY':None,
			'X-ASSISTANT':None,
			'X-MANAGER':None,
			'X-SPOUSE':None,
			'X-GENDER':None,
			'X-WAB-GENDER':None,
			'X-AIM':None,
			'X-ICQ':None,
			'X-GOOGLE-TALK':None,
			'X-GTALK':None,
			'X-JABBER':None,
			'X-MSN':None,
			'X-YAHOO':None,
			'X-TWITTER':None,
			'X-SKYPE':None,
			'X-SKYPE-USERNAME':None,
			'X-GADUGADU':None,
			'X-GROUPWISE':None,
			'X-MS-IMADDRESS':None,
			'X-MS-CARDPICTURE':None,
			'X-MS-OL-DESIGN':None,
			'X-PHONETIC-FIRST-NAME':None,
			'X-PHONETIC-LAST-NAME':None
		}
		#self.raw = []
		return

	def extract_vcf(self,single_contact):
		# store raw list data in instance-specific variable
		self.raw = single_contact
		# each contact is list type
		for item in self.raw:
			if not item: continue
			# Check if key:value, assign local-scope variables
			if item.count(':') > 0:
				key = item.split(':')[0]
				value = item.split(':')[1]
			
			# Check if key;sub:value or key;pref:value
			if key.count(';') > 0:
				key = key.split(';')[0]
			
			# Check extracted key against dict keys, assigning value if found
			if key in self.info:
				# check if value is populated by a single entry, as str type, convert to list
				if type(self.info[key]) == str:
					self.info[key] = [self.info[key], value]
				# check if value is populated by multiple entries, as list type, appending additional
				elif type(self.info[key]) == list:
					self.info[key].append(value)
				# convert dict NoneType entry to str type
				else:
					self.info[key] = value
				
			# for unknown keys, send message to stdout
			elif item:
				print repr(item) + ' not found'
		return

	def extract_csv(self,single_contact):
		# store raw list data in instance-specific variable
		self.raw = single_contact
		if len(single_contact.split(',')) > 1:
			data,numbers = single_contact.split(',')[0],single_contact.split(',')[1:]
			self.info['TEL'] = numbers
		else:
			# just in case, split the string again
			data = single_contact.split(',')[0]
		self.info['FN'] = data
		# Family; Given; Middle; Prefix; Suffix.
		self.info['N'] = '{0};{1};;;'.format(' '.join(data.split(' ')[1:]),data.split(' ')[0])
		# automatically inject version as 2.1
		self.info['VERSION'] = '2.1'
		return

	def display_contact(self):
		# FN is the display-ready key
		print '\n### ' + self.info['FN']
		for key in self.info:
			# omit VERSION and N for brevity, FN for redundancy
			if key in ['VERSION','N','FN']: continue
			# omit all NoneType values, display only populated key:value pairs
			if self.info[key] is not None: print key + ' ' + repr(self.info[key])
		return

	def format_vcf(self):
		vcf = {k: v for k, v in self.info.items() if v is not None}
		return vcf

	def output_vcf(self):
		d = self.format_vcf()
		print 'BEGIN:VCARD'
		print 'VERSION:{0}'.format(d['VERSION'])
		for k in d:
			if k is not 'VERSION':
				if type(d[k]) == list:
					for v in d[k]: print '{0}:{1}'.format(k,v)
				else:
					print '{0}:{1}'.format(k,d[k])
		print 'END:VCARD'
		return

	def __str__(self):
		return '{0}'.format(self.__dict__)