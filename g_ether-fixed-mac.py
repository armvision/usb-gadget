#!/usr/bin/env python

######
## read serial number and use it to generate two MAC addresses in the
## locally administered rane
## use these MAC address to load the g_ether module
##
## must be run as root or the modprobe will fail
##
## run at the end of the boot sequence
## do not loaded g_ether (etc) prior to this script running
## this script will load it for you
######

## imports
import os


## globals
# these two prefixes will be used to generate MAC addresses from the serial number
# while you can use anything that is a valid partial MAc address, they must be
# different and to minimise the possibility of a conflict should be in the
# locally administered MAC address range (i.e. second digit is one of
# 2, 6, A, or E)
# do not include any : characters, just the hex digits
# if a prefix is 12 digits or longer the first 12 will be returned
# as the MAC address
PREFIX_1 = '02'
PREFIX_2 = '06'

# which module to load
MODULE = 'g_ether'
# any additional parameters
MODULE_EXTRAS = ''


## functions
## getserial function is from https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

def make_mac(prefix, serial):
  # prefix and serial are expected to be strings
  
  # get last 12 digits of serial
  short_serial = serial[-12:]
  # add prefix
  raw_mac = prefix + short_serial[len(prefix):]
  # format mac
  mac = ''
  for i in range(0, len(raw_mac), 2):
    mac += raw_mac[i:i + 2] + ':'
  # strip trailing ':'
  mac = mac[:-1]
  
  return mac

# main process
if __name__ == '__main__':
  serial = getserial()
  # get MAC addresses
  mac_1 = make_mac(PREFIX_1, serial)
  mac_2 = make_mac(PREFIX_2, serial)
  # create shell command
  cmd = 'modprobe %s host_addr=%s dev_addr=%s %s' % (MODULE, mac_1, mac_2, MODULE_EXTRAS)
  print 'Attempting ', cmd
  os.system(cmd)
    
    
