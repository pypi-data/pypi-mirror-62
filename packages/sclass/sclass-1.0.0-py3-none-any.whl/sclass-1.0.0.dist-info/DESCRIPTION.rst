# sclass

Simple module that allows you to create classes with the concept of Private and Public attributes and methods.

Just create your own class inheriting from `sclass`.
Private methods are recognized by the first character of the attribute being `'_'`

`
from sclass import sclass


class Test(sclass):
    def __init__(self):
        self.name = "lorenzo"
        self._surname = "bartolini"

    def publicmethod(self):
        return 'Public'

    def _privatemethod(self):
        return 'private'

x = Test()

print(x.name)
print(x.publicmethod())
print(x._surname)
print(x._privatemethod())
`

Last two instructions will raise a custom exception: `PrivateException`


