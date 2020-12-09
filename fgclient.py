import socket
import time
import logging
from warnings import warn

fgclient_logger = logging.getLogger('fgclient')

class FgClient:

  def __init__(self,host='127.0.0.1',port=5051,savelog=True):
    self._logger = None
    if savelog:
      self.init_logger()
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host,port))
    self.term = bytes([13,10])
    msg = b'data'+self.term
    self.sock.sendall(msg)
    self._tic = None

  def init_logger(self):
    self._logger = logging.getLogger('fgclient')
    self._logger.setLevel(logging.INFO)
    self._logger.handlers = [] # turn off hanging files
    filehandler = logging.FileHandler('logs/fglog'+time.strftime('%y%m%d%H%M%S')+'.csv')
    self._logger.addHandler(filehandler)

  def tic(self):
    self._tic = time.time()

  def toc(self,time_step):
    if self._tic:
      sleep_time = self._tic + time_step - time.time()
      if sleep_time>0.0:
        time.sleep(sleep_time)
      else:
        warn('time step overrun {0:4.2f}/{1:4.2f}'.format(time_step-sleep_time,time_step))

  def _get_prop(self,prop_name):
    msg = bytes('get '+prop_name,encoding='utf8')+self.term
    self.sock.sendall(msg)
    data = self.sock.recv(1024)
    if self._logger:
      self._logger.debug('{},{},{},G'.format(time.time(),prop_name,str(data)))
    return(data)

  def get_prop_str(self,prop_name):
    return(str(self._get_prop(prop_name)))

  def get_prop_float(self,prop_name):
    res = float(self._get_prop(prop_name))
    if self._logger:
      self._logger.info('{},{},{},G'.format(time.time(),prop_name,res))
    return(res)

  def set_prop(self,prop_name,new_value):
    st = 'set {} {}'.format(prop_name,new_value)
    msg = bytes(st,encoding='utf8')+self.term
    self.sock.sendall(msg)
    if self._logger:
      self._logger.info('{},{},{},S'.format(time.time(),prop_name,new_value))

  def log_entry(self,log_name,value):
    if self._logger:
      self._logger.info('{},{},{},L'.format(time.time(),log_name,value))

  def vertical_speed_fps(self):
    return(self.get_prop_float('/velocities/vertical-speed-fps'))

  def heading_deg(self):
    return(self.get_prop_float('/orientation/heading-deg'))

  def altitude_ft(self):
    return(self.get_prop_float('/position/altitude-ft'))

  def get_elevator(self):
    return(self.get_prop_float('/controls/flight/elevator'))
  
  def get_aileron(self):
    return(self.get_prop_float('/controls/flight/aileron'))
  
  def set_elevator(self,val):
    self.set_prop('/controls/flight/elevator',val)
  
  def set_aileron(self,val):
    self.set_prop('/controls/flight/aileron',val)

  def ap_pitch_off(self):
    self.set_prop('/autopilot/locks/altitude','')
  
  def ap_pitch_vs(self,vs=0.0):
    self.set_prop('/autopilot/locks/altitude','vertical-speed-hold')
    self.set_prop('/autopilot/settings/vertical-speed-fpm',vs)
  
  def ap_roll_off(self):
    self.set_prop('/autopilot/locks/heading','')
  
  def ap_roll_hdg(self,hdg):
    self.set_prop('/autopilot/locks/heading','dg-heading-hold')
    self.set_prop('/autopilot/settings/heading-bug-deg',hdg)
  
# little test routine: set autopilot on and print key data
if __name__=="__main__":
  c = FgClient()
  # centre controls
  c.set_elevator(0.0)
  c.set_aileron(0.0)
  # AP on level and south
  c.ap_pitch_vs()
  c.ap_roll_hdg(180.0)
  while True:
    print(c.altitude_ft(),c.vertical_speed_fps(),c.heading_deg())
