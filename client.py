import socket

HOST='127.0.0.1'
PORT=5051

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
print('Connected')
term = bytes([13,10])
msg = b'data'+term
s.sendall(msg)
print('Sent',msg)

while True:
  # GET
  msg = b'get /position/altitude-ft'+term
  s.sendall(msg)
  print('Sent',msg)
  data = s.recv(1024)
  print('Received',repr(data))
  print(float(data))
  # SET
  u = -0.01*(1500-float(data))
  str = 'set /controls/flight/elevator {}'.format(u)
  msg = bytes(str,encoding='utf8')+term
  s.sendall(msg)
  print('Sent',msg)
