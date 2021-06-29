import pyping
r=pyping.ping('google.com')
if r.ret_code ==0:
    print("Sucess")
else:
    print("Failed with{}".format(r.ret_code))