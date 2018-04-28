import netifaces
import getpass
import socket
import os


def currentDir():
  dir = os.getcwd()
  dir = dir.replace("/home/" + username(), "~")
  return dir


def getIPs():
  ips = []
  for iface in netifaces.interfaces():
    addresses = netifaces.ifaddresses(iface)
    if 2 in addresses:
      for addr2 in addresses[2]:
        if 'addr' in addr2:
          if addr2['addr'] != '127.0.0.1':
            ips.append(addr2['addr'])
  return ips


def username():
  return getpass.getuser()


def machinename():
  return socket.gethostname()