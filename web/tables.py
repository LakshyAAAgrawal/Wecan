from flask_table import Table, Col, LinkCol

class MyTable(Table):
	classes = ["table table-hover"]
	first = Col('First')
	last = LinkCol('Edit', 'retry', url_kwargs=dict(editable="editable"), anchor_attrs={'class': 'myclass'})
	handle = Col('Handle')

	def get_tr_attrs(self, item):
		if item.editable:
			return {"class": "table-primary"}
		else:
			return {}

class Person(object):
	def __init__(self, first, last, handle, editable):
		self.first = first
		self.last = last
		self.handle = handle
		self.editable = editable