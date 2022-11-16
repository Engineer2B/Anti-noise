__author__ = 'Boris Breuer'


class printStatement:

	@staticmethod
	def arbitraryobject(obj):
		if type(obj) == dict:
			for k, v in obj.items():
				if hasattr(v, '__iter__'):
					print(k)
					printStatement.arbitraryobject(v)
				else:
					print('%s : %s' % (k, v))
		elif type(obj) == list:
			for v in obj:
				if hasattr(v, '__iter__'):
					print(' ')
					printStatement.arbitraryobject(v)
				else:
					print(v)
		else:
			print(obj)
