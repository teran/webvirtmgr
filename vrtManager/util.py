#
# Copyright (C) 2013 Webvirtmgr.
#

import random
import libxml2

def randomMAC():
    """Generate a random MAC address."""

    oui = [ 0x52, 0x54, 0x00 ] # qemu MAC

    mac = oui + [
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def randomUUID():
    """Generate a random UUID."""

    u = [ random.randint(0, 255) for dummy in range(0, 16) ]
    return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2, "%02x" * 6]) % tuple(u)

def get_max_vcpus(conn, type=None):
    """@param conn: libvirt connection to poll for max possible vcpus
       @type type: optional guest type (kvm, etc.)"""
    if type is None:
        type = conn.getType()
    try:
        m = conn.getMaxVcpus(type.lower())
    except libvirt.libvirtError:
        m = 32
    return m

def get_phy_cpus(conn):
    """Get number of physical CPUs."""
    hostinfo = conn.getInfo()
    pcpus = hostinfo[4] * hostinfo[5] * hostinfo[6] * hostinfo[7]
    return pcpus

def xml_escape(str):
    """Replaces chars ' " < > & with xml safe counterparts"""
    if str is None:
        return None

    str = str.replace("&", "&amp;")
    str = str.replace("'", "&apos;")
    str = str.replace("\"", "&quot;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    return str

def compareMAC(p, q):
    """Compare two MAC addresses"""
    pa = p.split(":")
    qa = q.split(":")

    if len(pa) != len(qa):
        if p > q:
            return 1
        else:
            return -1

    for i in xrange(len(pa)):
        n = int(pa[i], 0x10) - int(qa[i], 0x10)
        if n > 0:
            return 1
        elif n < 0:
            return -1
    return 0

def get_xml_path(xml, path=None, func=None):
    """
    Return the content from the passed xml xpath, or return the result
    of a passed function (receives xpathContext as its only arg)
    """
    doc = None
    ctx = None
    result = None

    try:
        doc = libxml2.parseDoc(xml)
        ctx = doc.xpathNewContext()

        if path:
            ret = ctx.xpathEval(path)
            if ret != None:
                if type(ret) == list:
                    if len(ret) >= 1:
                        result = ret[0].content
                else:
                    result = ret

        elif func:
            result = func(ctx)

        else:
            raise ValueError(_("'path' or 'func' is required."))
    finally:
        if doc:
            doc.freeDoc()
        if ctx:
            ctx.xpathFreeContext()
    return result

