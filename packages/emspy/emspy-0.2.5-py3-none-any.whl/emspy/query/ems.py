from __future__ import absolute_import
from .asset import Asset


class EMS(Asset):
	'''Retrieves EMS system-specific info'''

	def __init__(self, conn):
		Asset.__init__(self, conn, "EMS")


	def update_list(self):
		Asset.update_list(self, uri_keys=('ems_sys', 'list'))


	def ensure_loaded(self):
		if not (Asset.list_all(self)):
			self.update_list()


	def get_id(self, name = None):

		# Support using integer IDs directly
		if isinstance(name, int):
			return name
		
		self.ensure_loaded()
		name = name.upper()
		a    = self.search('name', name, searchtype="match")['id'].tolist()
		return a if len(a) > 1 else a[0]


	def get_name(self, id_val = None):
		self.ensure_loaded()
		a = self.search('id', id_val, searchtype="match")['name'].tolist()
		return a if len(a) > 1 else a[0]


