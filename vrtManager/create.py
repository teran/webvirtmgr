#
# Copyright (C) 2013 Webvirtmgr.
#
import virtinst
from vrtManager import util


class wvmCreate(object):
    def __init__(self, host, login, passwd, conn):
        self.wvm = objconn

    def get_guest_cap(self):
        """Get guest capabilities"""
        return virtinst.CapabilitiesParser.guest_lookup(self.wvm)

    def create(self, name, ram, cpu, nets, virtio, storages):
        """
        Create VM function

        """
        ram = int(ram) * 1024

        xml = """
                <domain type='%s'>
                  <name>%s</name>
                  <uuid>%s</uuid>
                  <memory>%s</memory>
                  <currentMemory>%s</currentMemory>
                  <vcpu>%s</vcpu>""" % (domain, name, uuid, memory, memory, vcpu)

        if host_model:
            xml += """<cpu mode='host-model'/>"""

        xml += """<os>
                    <type arch='%s'>hvm</type>
                    <boot dev='hd'/>
                    <boot dev='cdrom'/>
                    <bootmenu enable='yes'/>
                  </os>""" % (arch)

        xml += """<features>
                    <acpi/><apic/><pae/>
                  </features>
                  <clock offset="utc"/>
                  <on_poweroff>destroy</on_poweroff>
                  <on_reboot>restart</on_reboot>
                  <on_crash>restart</on_crash>
                  <devices>"""

        xml += """  <disk type='file' device='disk'>
                      <driver name='qemu' type='raw'/>
                      <source file='/var/lib/libvirt/images/qqqq.img'/>
                      <target dev='sda' bus='ide'/>
                    </disk>"""

        xml += """  <disk type='file' device='cdrom'>
                      <driver name='qemu' type='raw'/>
                      <source file=''/>
                      <target dev='hda' bus='ide'/>
                      <readonly/>
                    </disk>"""

        xml += """  <interface type='network'>
                      <source network='default'/>
                      <mac address='52:54:00:dd:18:7e'/>
                    </interface>"""

        xml += """  <input type='mouse' bus='ps2'/>
                    <graphics type='vnc' port='-1'/>
                    <console type='pty'/>
                    <video>
                      <model type='cirrus'/>
                    </video>
                  </devices>
                </domain>"""

        disks = []
        for image in images:
            img = self.storageVolPath(image)
            image_type = self.get_vol_image_type(storages, img.name())
            disks.append({'image': image, 'type': image_type})

        xml = """<domain type='%s'>
                  <name>%s</name>
                  <description>None</description>
                  <memory unit='KiB'>%s</memory>
                  <vcpu>%s</vcpu>""" % (dom_type, name, ram, cpu)

        if host_model:
            xml += """<cpu mode='host-model'/>"""

        xml += """<os>
                    <type arch='x86_64' machine='%s'>hvm</type>
                    <boot dev='hd'/>
                    <boot dev='cdrom'/>
                    <bootmenu enable='yes'/>
                  </os>
                  <features>
                    <acpi/>
                    <apic/>
                    <pae/>
                  </features>
                  <clock offset='utc'/>
                  <on_poweroff>destroy</on_poweroff>
                  <on_reboot>restart</on_reboot>
                  <on_crash>restart</on_crash>
                  <devices>
                    <emulator>%s</emulator>""" % (machine, emulator)

        disk_letters = list(string.lowercase)
        for disk in disks:
            xml += """<disk type='file' device='disk'>
                          <driver name='qemu' type='%s'/>
                          <source file='%s'/>""" % (disk['type'], disk['image'])
            if virtio:
                xml += """<target dev='vd%s' bus='virtio'/>""" % (disk_letters.pop(0),)
            else:
                xml += """<target dev='hd%s' bus='ide'/>""" % (disk_letters.pop(0),)

            xml += """</disk>"""

        xml += """<disk type='file' device='cdrom'>
                      <driver name='qemu' type='raw'/>
                      <source file=''/>
                      <target dev='sda' bus='ide'/>
                      <readonly/>
                    </disk>"""

        for net in nets.split(','):
            xml += """
                    <interface type='network'>
                        <source network='%s'/>""" % net
            if virtio:
                xml += """<model type='virtio'/>"""
            xml += """
                    </interface>"""

        xml += """
                    <input type='tablet' bus='usb'/>
                    <input type='mouse' bus='ps2'/>
                    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0' passwd='%s'>
                      <listen type='address' address='0.0.0.0'/>
                    </graphics>
                    <memballoon model='virtio'/>
                  </devices>
                </domain>""" % (passwd)
        self.wvm.defineXML(xml)
        dom = self.lookupVM(name)
        dom.setAutostart(1)