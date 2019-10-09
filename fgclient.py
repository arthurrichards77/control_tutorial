import socket

class FgClient:

  def __init__(self,host='127.0.0.1',port=5051):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host,port))
    #print('Connected')
    self.term = bytes([13,10])
    msg = b'data'+self.term
    self.sock.sendall(msg)

  def _get_prop(self,prop_name):
    msg = bytes('get '+prop_name,encoding='utf8')+self.term
    self.sock.sendall(msg)
    #print('Sent',msg)
    data = self.sock.recv(1024)
    #print('Received',repr(data))
    return(data)

  def get_prop_str(self,prop_name):
    return(str(self._get_prop(prop_name)))

  def get_prop_float(self,prop_name):
    return(float(self._get_prop(prop_name)))

  def set_prop(self,prop_name,new_value):
    st = 'set {} {}'.format(prop_name,new_value)
    msg = bytes(st,encoding='utf8')+self.term
    self.sock.sendall(msg)
    #print('Sent',msg)

  def vertical_speed_fps(self):
    return(self.get_prop_float('/velocities/vertical-speed-fps'))

  def heading_deg(self):
    return(self.get_prop_float('/orientation/heading-deg'))

  def altitude_ft(self):
    return(self.get_prop_float('/position/altitude-ft'))
  
# little test routine: set autopilot on and print altitude
if __name__=="__main__":
  c = FgClient()
  c.set_prop('/autopilot/locks/altitude','vertical-speed-hold')
  c.set_prop('/autopilot/settings/vertical-speed-fpm',0.0)
  c.set_prop('/autopilot/locks/heading','dg-heading-hold')
  c.set_prop('/autopilot/settings/heading-bug-deg',180.0)
  while True:
    print(c.altitude_ft(),c.vertical_speed_fps(),c.heading_deg())
