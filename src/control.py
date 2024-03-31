import domain as domain
import storage

def addProfile(p:domain.profile):
    data = storage.read()
    data.profiles.append(p)
    storage.write(data)