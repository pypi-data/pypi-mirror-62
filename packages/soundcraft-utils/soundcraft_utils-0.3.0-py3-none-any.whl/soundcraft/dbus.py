import soundcraft
import soundcraft.notepad
import argparse
import os.path
import sys
from string import Template
try:
    import gi
except ModuleNotFoundError:
    print("\nThe PyGI library must be installed from your distribution; usually called python-gi, python-gobject, or pygobject\n")
    raise
gi.require_version('GUdev', '1.0')
from gi.repository import GLib
from gi.repository import GUdev
from pydbus import SystemBus
from pydbus.generic import signal

BUSNAME='soundcraft.utils.notepad'

class NotepadDbus(object):
    """
      <node>
        <interface name='soundcraft.utils.notepad.device'>
          <property name='name' type='s' access='read' />
          <property name='fixedRouting' type='a{ss}' access='read' />
          <property name='routingTarget' type='s' access='read' />
          <property name='sources' type='as' access='read' />
          <property name='routingSource' type='s' access='readwrite'>
            <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
          </property>
        </interface>
      </node>
    """

    InterfaceName = 'soundcraft.utils.notepad.device'

    def __init__(self, dev):
        self._dev = dev

    @property
    def name(self):
        return self._dev.name

    @property
    def fixedRouting(self):
        return self._dev.fixedRouting

    @property
    def routingTarget(self):
        return self._dev.routingTarget

    @property
    def sources(self):
        return self._dev.sources

    @property
    def routingSource(self):
        return self._dev.routingSource

    @routingSource.setter
    def routingSource(self, request):
        self._dev.routingSource = request
        self.PropertiesChanged(self.InterfaceName, {"routingSource": self.routingSource}, [])

    PropertiesChanged = signal()

class Service:
    """
      <node>
        <interface name='soundcraft.utils.notepad'>
          <property name='version' type='s' access='read' />
          <property name='devices' type='ao' access='read'>
            <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
          </property>
          <signal name='Added'>
            <arg name='path' type='o'/>
          </signal>
          <signal name='Removed'>
            <arg name='path' type='o'/>
          </signal>
          <method name='Shutdown'/>
        </interface>
      </node>
    """

    InterfaceName = 'soundcraft.utils.notepad'
    PropertiesChanged = signal()
    Added = signal()
    Removed = signal()

    def __init__(self):
        self.object = None
        self.bus = SystemBus()
        self.udev = GUdev.Client(subsystems = ["usb/usb_device"])
        self.udev.connect('uevent', self.uevent)
        self.loop = GLib.MainLoop()
        self.busname = self.bus.publish(BUSNAME, self)

    def run(self):
        self.tryRegister()
        if not self.hasDevice():
            print(f"Waiting for one to arrive...")
        self.loop.run()

    @property
    def version(self):
        return soundcraft.__version__

    @property
    def devices(self):
        if self.hasDevice():
            return [self.object._path]
        return []

    def Shutdown(self):
        print("Shutting down")
        self.unregister()
        self.loop.quit()

    def objPath(self, idx):
        return f"/soundcraft/utils/notepad/{idx}"

    def tryRegister(self):
        if self.hasDevice():
            print(f"There is already a {self.object._wrapped._dev.name} on the bus at {self.object._path}")
            return
        dev = soundcraft.notepad.autodetect()
        if dev is None:
            print(f"No recognised device was found")
            return
        path = self.objPath(0)
        wrapped = NotepadDbus(dev)
        self.object = self.bus.register_object(path, wrapped, None)
        self.object._wrapped = wrapped
        self.object._path = path
        print(f"Presenting {self.object._wrapped._dev.name} on the system bus as {path}")
        self.Added(path)
        self.PropertiesChanged(self.InterfaceName, {"devices": self.devices}, [])

    def hasDevice(self):
        return self.object is not None

    def unregister(self):
        if not self.hasDevice():
            return
        path = self.object._path
        print(f"Removed {self.object._wrapped._dev.name} AKA {path} from the system bus")
        self.object.unregister()
        self.object = None
        self.PropertiesChanged(self.InterfaceName, {"devices": self.devices}, [])
        self.Removed(path)

    def uevent(self, observer, action, device):
        if action == 'add':
            idVendor = device.get_property('ID_VENDOR_ID')
            idProduct = device.get_property('ID_PRODUCT_ID')
            if idVendor == "05fc":
                print(f"Checking new Soundcraft device ({idVendor}:{idProduct})...")
                self.tryRegister()
                if not self.hasDevice():
                    print(f"Contact the developer for help adding support for your advice")
        elif action == 'remove' and self.hasDevice():
            # UDEV adds leading 0s to decimal numbers.  They're not octal.  Why??
            busnum = int(device.get_property('BUSNUM').lstrip("0"))
            devnum = int(device.get_property('DEVNUM').lstrip("0"))
            if busnum == self.object._wrapped._dev.dev.bus and devnum == self.object._wrapped._dev.dev.address:
                self.unregister()

def findDbusFiles():
    result = {}
    modulepaths = soundcraft.__path__
    for path in modulepaths:
        dbusdatapath = os.path.join(path, 'data/dbus-1')
        result[dbusdatapath] = []
        for path, dirs, files in os.walk(dbusdatapath):
            if not files:
                continue
            for fname in files:
                relative = os.path.relpath(os.path.join(path, fname), start=dbusdatapath)
                result[dbusdatapath].append(relative)
    return result

def serviceExePath():
    exename = sys.argv[0]
    exename = os.path.abspath(exename)
    if exename.endswith(".py"):
        raise ValueError("Running setup out of a module-based execution is not supported")
    return exename

def setup(cfgroot="/usr/share/dbus-1"):
    templateData = {
        'dbus_service_bin': serviceExePath(),
        'busname': BUSNAME,
    }
    sources = findDbusFiles()
    for (srcpath, files) in sources.items():
        for fname in files:
            src = os.path.join(srcpath, fname)
            dst = os.path.join(cfgroot, fname)
            print(f"Installing {src} -> {dst}")
            with open(src, "r") as srcfile:
                srcTemplate = Template(srcfile.read())
                with open(dst, "w") as dstfile:
                    dstfile.write(srcTemplate.substitute(templateData))
    print(f"Starting service version {soundcraft.__version__}...")
    client = Client()
    print(f"Setup is complete.")
    print(f"Run soundcraft_gui or soundcraft_cli as a regular user")

class DbusInitializationError(RuntimeError):
    pass

class VersionIncompatibilityError(DbusInitializationError):
    def __init__(self, serviceVersion, pid, clientVersion):
        super().__init__(f"Running service version {serviceVersion} (PID {pid}) is incompatible with the client version {clientVersion} - Kill and restart the dbus service")

class DbusServiceSetupError(DbusInitializationError):
    def __init__(self):
        super().__init__(f"No dbus service found for {BUSNAME} - Run 'soundcraft_dbus_service --setup' as root to enable it")

class Client:
    MGRPATH = '/soundcraft/utils/notepad'

    def __init__(self, added_cb = None, removed_cb = None):
        self.bus = SystemBus()
        self.dbusmgr = self.bus.get('.DBus')
        self.dbusmgr.onNameOwnerChanged = self._nameChanged
        self.manager = None
        self.initManager()
        self.ensureServiceVersion(allowRestart=True)
        if removed_cb is not None:
            self.deviceRemoved.connect(removed_cb)
        if added_cb is not None:
            self.deviceAdded.connect(added_cb)
            self.autodetect()

    def initManager(self):
        try:
            self.manager = self.bus.get(BUSNAME, self.MGRPATH)
            self.manager.onAdded = self._onAdded
            self.manager.onRemoved = self._onRemoved
        except Exception as e:
            if 'org.freedesktop.DBus.Error.ServiceUnknown' in e.message:
                raise DbusServiceSetupError()
            raise e

    def servicePid(self):
        return self.dbusmgr.GetConnectionUnixProcessID(BUSNAME)

    def serviceVersion(self):
        return self.manager.version

    def ensureServiceVersion(self, allowRestart=False):
        mgrVersion = self.serviceVersion()
        localVersion = soundcraft.__version__
        if mgrVersion != localVersion:
            if not callable(getattr(self.manager, 'Shutdown', None)) or not allowRestart:
                raise VersionIncompatibilityError(mgrVersion, self.servicePid(), localVersion)
            else:
                self.restartService(mgrVersion, localVersion)
                self.ensureServiceVersion(allowRestart=False)

    def restartService(self, mgrVersion, localVersion):
        loop = GLib.MainLoop()
        with self.serviceDisconnected.connect(loop.quit):
            print(f"Restarting soundcraft dbus service ({self.servicePid()}) to upgrade {mgrVersion}->{localVersion}")
            self.manager.Shutdown()
            loop.run()
        self.initManager()
        print(f"Restarted the service at {self.servicePid()}")

    serviceConnected = signal()

    serviceDisconnected = signal()

    def _nameChanged(self, busname, old, new):
        if busname != BUSNAME:
            return
        if old == '':
            print(f"New {busname} connected")
            self.serviceConnected()
        elif new == '':
            print(f"{busname} service disconnected")
            self.serviceDisconnected()

    def autodetect(self):
        devices = self.manager.devices
        if not devices:
            return None
        proxyDevice = self.bus.get(BUSNAME, devices[0])
        self.deviceAdded(proxyDevice)
        return proxyDevice

    def waitForDevice(self):
        loop = GLib.MainLoop()
        with self.manager.Added.connect(lambda path: loop.quit()):
            loop.run()
        return self.autodetect()

    deviceAdded = signal()

    def _onAdded(self, path):
        proxyDevice = self.bus.get(BUSNAME, path)
        self.deviceAdded(proxyDevice)

    deviceRemoved = signal()

    def _onRemoved(self, path):
        self.deviceRemoved(path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", help="Set up the dbus configuration in /usr/share/dbus-1 (Must be run as root)", action="store_true")
    args = parser.parse_args()
    if args.setup:
        setup()
    else:
        service = Service()
        service.run()

if __name__ == '__main__':
    main()
