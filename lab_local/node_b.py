import argparse,socket,threading
p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=4242);p.add_argument('--upstream-host',default='127.0.0.1');p.add_argument('--upstream-port',type=int,default=4243);a=p.parse_args();s=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);s.bind((a.host,a.port));s.listen(8)
def h(c):
 with c:
  u=socket.create_connection((a.upstream_host,a.upstream_port),timeout=5)
  with u:u.sendall(c.recv(8192));c.sendall(u.recv(8192))
while True:c,_=s.accept();threading.Thread(target=h,args=(c,),daemon=True).start()
