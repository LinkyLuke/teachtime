import unittest
from faker import Faker 

class TestUsers(unittest.TestCase):

	def setUp(self):
		fake = Faker()
		self.user_1 = fake.seed(1463)
		self.email_1 = 'test@email.com'
		db.session.add(self.user_1)
		de.session.add(self.email_1)
		db.session.commit()

	def tearDown(self):
		db.session.delete(self.user_1)
		db.session.delete(self.emal_1)
		
if __name__ == '__main__':
	unittest.main()