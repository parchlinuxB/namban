# In the name of god

from gi.repository import Gdk, Gtk
import settings
import domain as domain
from pathlib import Path
from .textCheck import isIp,baseCheck

class trashIcon(Gtk.Image):
    def __init__(self):
        super().__init__()
        self.set_from_icon_name("trash-empty")
        # self.set_size_request(15,15)

class pencilIcon(Gtk.Image):
    def __init__(self):
        super().__init__()
        self.set_from_icon_name("draw-freehand")

class profileConnectButton(Gtk.Switch):
    def __init__(self, app:domain.app, profile:domain.profile, default=False):
        super().__init__()
        self.app = app
        self.domain = profile
        self.add_css_class('server-button')
        self.set_state(default)
        self.connect("state-set", self.onChange)
    def onChange(self, _, state):
        if state:
            self.app.connectProfile(self.domain)
        else:
            self.app.disconnectProfiles()
    

class Label(Gtk.Label):
    def __init__(self,label,classes=[],maxChar=None,**more):
        if maxChar:
            if label.__len__() > maxChar:
                if maxChar > 2 : 
                    label = label[:maxChar-2] + ".."
                else :
                    label = label[:maxChar]
        super().__init__(label=label,**more)
        self.set_css_classes(classes+['label'])

class LeftFloat(Gtk.AspectFrame):
    def __init__(self,widget):
        super().__init__(
            halign=Gtk.Align.START,
            obey_child=True
        )
        self.set_child(widget)

class centerFloat(Gtk.AspectFrame):
    def __init__(self,widget):
        super().__init__(
            halign=Gtk.Align.CENTER,
            xalign=0.5,
            yalign=0.5,
            # ratio=1.0,
            obey_child=True
        )
        self.set_child(widget)

class Fixed(Gtk.Fixed):
    def __init__(self,classes=[]):
        super().__init__()
        self.set_css_classes(classes)
    def put(self, widget, x, y):
        super().put(widget, x, y)
        return self

class profileInformation(Gtk.Fixed):
    def __init__(self,profile:domain.profile):
        super().__init__()
        self.prof = profile
        self.update()
        self.add_css_class('server-information')
    def update(self):
        try:
            self.remove(self.title)
            self.title = None
            self.remove(self.inform)
            self.inform = None
        except:...

        self.title = Label(
            self.prof.name,
            classes=[
                'color-high',
                'font-l'
                ],
            maxChar=11
            )
        serversAspectFrame = Gtk.AspectFrame()
        serversAspectFrame.add_css_class('server-aspect-frame')
        self.servers = Gtk.Grid()
        serversAspectFrame.set_child(
            self.servers
        )
        servers = [self.prof.server1]
        if self.prof.server2: servers.append(self.prof.server2)
        for i, serv in enumerate(servers):
            self.servers.attach(
                LeftFloat(
                    Label(
                        f'{i+1}: {str(serv)}',
                        classes=['font-s','color-low']
                    )
                ),0,i,1,1
            )
        self.put(
            self.title,
            0,5
        )
        self.put(
            serversAspectFrame,
            80,0
        )

class Button(Gtk.Button):
    def __init__(self, child, onClick=lambda*_:... , classes=[],size=None,enable=True):
        super().__init__()
        self.set_child(child)
        self.set_css_classes(['button'] + classes)
        # self.set_relief(Gtk.ReliefStyle.NONE)
        if size:
            self.set_size_request(*size)
            self.set_hexpand(False)
            self.set_vexpand(False)
        self.connect('clicked', onClick)
        self.set_sensitive(enable)
    def enable_css(self, className):
        if className not in self.get_css_classes():
            self.add_css_class(className)
    def disable_css(self, className):
        while className in self.get_css_classes():
            self.remove_css_class(className)
    def enable(self):
        self.set_sensitive(True)
    def disable(self):
        self.set_sensitive(False)

class profile(Gtk.Box):
    def __init__(self,app:domain.app,profile:domain.profile):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.add_css_class('server')
        self.fixed = Gtk.Fixed()
        self.app = app
        self.domain = profile
        self.append(
            self.fixed
        )
        self.connectButton = profileConnectButton(app,profile)
        self.fixed.put(
            self.connectButton,
            235,4
        )
        self.fixed.put(
            Button(
                trashIcon(),lambda *_:self.app.deleteProfile(profile),[]
            )
            ,
            189,0
        )
        self.fixed.put(
            Button(
                pencilIcon(),lambda *_ : self.app.window.goEdit(profile,lambda newp : self.app.editProfile(profile, self.app.window.editor.dumpProfToInput(newp)) ),[]
            )
            ,
            150,0
        )
        self.fixed.put(
            profileInformation(profile),
            10,0
        )
        self.update()
    def update(self):
        self.connectButton.set_state(
            self.app.connectedProfile == self.domain
        )

class Grid(Gtk.Grid):
    def empty (self):
        children = self.get_children()
        for child in children:
            self.remove(child)

class profileList(Grid):
    def __init__(self, app:domain.app):
        super().__init__()
        self.add_css_class('server-list')
        self.app = app
        self.profs = []
        self.start()

    def start(self):
        for i, p in enumerate(self.app.data.profiles):
            prof = profile(self.app,p)
            self.profs.append(prof)
            self.attach(
                prof,
                0,i,1,1
            )
    
    def restart(self):
        self.remove_column(0)
        self.profs = []
        self.start()

    def update(self):
        for current in self.profs:
            if current.domain not in self.app.data.profiles:
                self.restart()
        for featue in self.app.data.profiles:
            if featue not in list(map(lambda x:x.domain, self.profs)):
                self.restart()
        for ch in self.profs:
            ch.update()

class addButton(Gtk.Overlay):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.button = Button(Label('+'),self.click)
        self.button.set_css_classes(['add-btn'])
        self.set_child(self.button)
    def click(self, *_):
        self.app.window.goEdit(None, lambda data: self.app.addProfile(
            domain.profile(
                server1=domain.server(url=data['server1'],type='dns'),
                server2=domain.server(url=data['server2'],type='dns') if data.get('server2',False) else None,
                name=data['name']
            )
            ))

class mainWindowContainer(Gtk.Fixed):
    def __init__(self, app):
        super().__init__()
        self.childs = [profileList(app)]
        self.put(
            self.childs[0],0,0
        )
        self.put(
            addButton(app),10,350
        )
    def update(self):
        for ch in self.childs:
            ch.update()


class Input(Gtk.Entry):
    def __init__(self,app=None,name="",optional=False,placeholder=None,classes=[],onchange=None,checker=lambda *_:True):
        super().__init__()
        self.set_size_request(250,20)
        self.app = app
        self.set_css_classes(['input'] + classes)
        self.name = name
        self.optional = optional
        if placeholder:
            self.set_placeholder_text(placeholder)
        if onchange:
            self.connect("changed", onchange)
        self.checker = checker

class Form:
    def __init__(self, *inputs:list[Input]) -> None:
        self.inputs = inputs
    class LowEntryError(Exception):
        def __init__(self, *entries):
            super().__init__()
            self.inputs = entries
    def read(self):
        empties = []
        for i in self.inputs:
            i:Input
            t:str = i.get_text()
            if t.strip() == '':
                if not i.optional:
                    empties.append(i)
            else:
                if not i.checker(t):
                    empties.append(i)

        if empties:
            raise self.LowEntryError(*empties)
        return {
            i.name: i.get_text() for i in self.inputs
        }
    def write(self, data:dict):
        for inp in self.inputs:
            try:
                if not data:
                    inp.set_text("")
                elif inp.name in data:
                    inp.set_text(data[inp.name])
               
            except:...

class editWindowContainer(Gtk.Box):
    def handleOK (self, *args):
        # self.then(self.data)
        self.app.window.goMain()
    def set_entries(self, baseData ,then):
        self.form.write(baseData)
        self.then = then
    def __init__(self,app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app
        self.inputs = [
            Input(self.app, "name", onchange=self.update, classes=['mt-6'], placeholder="Name"),
            Input(self.app, "server1",onchange=self.update, classes=['mt-2'], checker=isIp(),placeholder="Server 1"),
            Input(self.app, "server2",onchange=self.update, classes=['mt-2'], checker=isIp(),placeholder="Server 2 (optional)", optional=True)
        ]
        self.form = Form(*self.inputs)
        for i in self.inputs : self.append(centerFloat(i))
        self.okbtn = Button(Label("Ok"),self.ok, classes=['mb-1'], enable=False)
        self.canbtn = Button(Label("Cancel"),self.cancel, classes=['mb-1', 'bg-red'])
        self.append(
            centerFloat(
                Fixed(classes=['mt-3'])
                    .put(
                        self.okbtn, 10, 0
                    )
                    .put(
                        self.canbtn, 60, 0
                    )
            )
        )        
    def update(self,*_):
        try:
            data = self.form.read()
            self.okbtn.enable()
            self.okbtn.enable_css("bg-green")
        except Form.LowEntryError as e:
            self.okbtn.disable()
            self.okbtn.disable_css("bg-green")
    def ok(self,*_):
        try:
            data = self.form.read()
            if self.then:
                self.then(data)
        except:
            ...
        self.set_entries(None, None)
        self.back()
 
    def cancel(self,*_):
        self.set_entries(None, None)
        self.back()
 
    def back(self):
        self.app.window.goMain()

    def loadProfFromInput(self, prof):
        r = {
            "name":prof.name,
            "server1":prof.server1.url
        }
        if prof.server2:
            r['server2'] = prof.server2.url
        return r
    def dumpProfToInput(self,prof):
        wargs = {
            "name":prof['name'],
            "server1":self.app.loadServ({'url':prof['server1'],'type':'dns'})
        }
        if prof.get('server2',False).strip():
            wargs['server2'] = self.app.loadServ({'url':prof['server2'],'type':'dns'})
        return domain.profile(**wargs)



class Stack(Gtk.Stack):
    def __init__(self,**data):
        super().__init__()
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.data = data
        self.add(**data)
    def show(self,name):
        self.set_visible_child(
            self.data[name]
        )
    def add(self,**data):
        self.data = {
            **self.data,
            **data
        }
        for _, widget in data.items():
            Gtk.Stack.add_child(self,widget)


class window(Gtk.ApplicationWindow):
    def __init__(self, app=None):
        super().__init__(application=app, title=settings.WINDOW_TITLE)
        app.window = self
        self.app = app
        self.set_default_size(300,400)
        self.main = mainWindowContainer(app)
        self.editor = editWindowContainer(app)
        self.stack = Stack(
            main = self.main,
            editor = self.editor
        )
        self.set_child(
            self.stack
        )
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(
            str(Path(
                __file__
            ).parent / "style.css"
            )
        )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.goMain()
    def update(self):
        self.main.update()
    def goMain(self):
        self.update()
        self.stack.show('main')
    def goEdit(self, baseData=None, then=None):
        if isinstance(baseData,domain.profile):
            baseData = self.editor.loadProfFromInput(baseData)
        self.editor.set_entries(baseData, then)
        self.stack.show('editor')
__all__ = [
    window
]