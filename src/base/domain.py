class LowFields(Exception):
    def __init__(self, *fields):
        super().__init__(
            f"This fields is esential: {', '.join(fields)}"
        )
        self.fields = fields
class Field:
    def __init__(self, optional=False):
        self.optional = optional
        self.name = None
    def set_name(self,_name):
        self.name = _name
class Model:
    def __init_subclass__(cls) -> None:
        cls._fields:list[Field] = []
        for name, obj in cls.__dict__.items():
            if isinstance(obj, Field):
                obj.set_name(name)
                cls._fields.append(obj)
    def __init__(self,**wargs) -> None:
        errorFields = []
        for f in self._fields:
            if f.name not in wargs:
                if f.optional:
                    wargs[f.name] = None
                else :
                    errorFields.append(f)
        if errorFields :
            raise LowFields(*errorFields)
        for name, val in wargs.items():
            if name in list(map(lambda x:x.name, self._fields)): 
                setattr(
                    self, name, val
                )
    def __eq__(self,another):
        class oooooo1:...
        class oooooo2:...
        for f in self._fields:
            if getattr(self,f.name,oooooo1) != getattr(another,f.name,oooooo2):
                return False
        return True