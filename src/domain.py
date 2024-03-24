from base.domain import Model,Field

class server(Model):
    type = Field()
    url = Field()
    def __str__(self):
        return self.url

class profile(Model):
    server1 = Field()
    server2 = Field(optional=True)
    name = Field(optional=True)
    def __str__(self):
        return self.name | self.server1.__str__()


class appData:
    def __init__(self, profiles:list[server]) -> None:
        self.profiles = profiles
class app:
    def __init__(self, data:appData):
        self.data = data