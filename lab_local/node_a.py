import argparse,json,socket,time,random
p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=4242);p.add_argument('--scenario',default='classic');p.add_argument('--lora-sim',action='store_true');a=p.parse_args();
if a.lora_sim:time.sleep(random.uniform(0.1,0.3))
s=socket.create_connection((a.host,a.port),timeout=5);t=time.time();s.sendall((json.dumps({'scenario':a.scenario})+'\n').encode());d=s.recv(8192).decode().strip();print(f'[LINK] established in {time.time()-t:.3f}s');print(d)
