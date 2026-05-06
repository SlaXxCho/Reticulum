import argparse, json, socket

def evaluate(s):
    m={"classic":{"decision":"allow","profile":"classic","key_version":1},"hybrid_light":{"decision":"upgrade","profile":"hybrid_light","key_version":2,"pqc":"completed"},"max_security_block":{"decision":"block","reason":"required profile not available"},"replay":{"decision":"reject","reason":"replay rejected"},"key_desync":{"decision":"fail_safe","reason":"unexpected key_version"},"pqc_forced_fail":{"decision":"block","reason":"pqc upgrade failed","profile":"hybrid_light","key_version":1,"pqc":"failed"}}
    return {"ok":m.get(s,{"decision":"allow","profile":"classic","key_version":1})["decision"] in ("allow","upgrade"),**m.get(s,m["classic"]) }

def main():
 p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=4243);a=p.parse_args();srv=socket.socket();srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);srv.bind((a.host,a.port));srv.listen(8)
 while True:
  c,_=srv.accept();
  with c:
   raw=c.recv(8192).decode().strip();
   if raw:c.sendall((json.dumps(evaluate(json.loads(raw).get('scenario','classic')))+'\n').encode())
if __name__=='__main__':main()
