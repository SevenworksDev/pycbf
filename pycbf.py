import sys, itertools, hashlib, requests, time, random, base64, json, threading

try:
    conf = {}
    with open("cbf.config", 'r') as file:
        for line in file:
            key, value = line.strip().split('->')
            conf[key.strip()] = value.strip()
    un = str(conf.get('username'))
    pw = str(conf.get('password'))
    lvl = str(conf.get('levelID'))
except:
    input("CBFError: cbf.config file missing. Create one and use the following format shown below.\n\nusername->RobTop\npassword->DontHackMeLol\nlevelID->128\nprefix->/\nwait->2")
    sys.exit()

def comment_chk(*,username,comment,levelid,percentage,type):
  part_1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
  return base64.b64encode(xor(hashlib.sha1(part_1.encode()).hexdigest(),"29481").encode()).decode()
def xor(data, key):
  return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, itertools.cycle(key)))
def gjp_encrypt(data):
  return base64.b64encode(xor(data,"37526").encode()).decode()
def gjp_decrypt(data):
  return xor(base64.b64decode(data.encode()).decode(),"37526")

def getGJUsers(target):
  try:
    request = requests.post("http://www.boomlings.com/database/getGJUsers20.php",data={"secret":"Wmfd2893gb7","str":target},headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)
  except:
    print(f"CBFError: Fetching information for user {target} failed.")

def uploadComment(name,passw,comment,perc,level):
        try:
                accountid = getGJUsers(name)[1]
                gjp = gjp_encrypt(passw)
                c = base64.b64encode(comment.encode()).decode()
                chk = comment_chk(username=name,comment=c,levelid=str(level),percentage=perc,type="0")
                r = requests.post("http://www.boomlings.com/database/uploadGJComment21.php",data={"secret":"Wmfd2893gb7","accountID":accountid,"gjp":gjp,"userName":name,"comment":c,"levelID":level,"percent":perc,"chk":chk},headers={"User-Agent": ""}).text
                if r.startswith("temp_"):
                    reason = r.split("_")
                    print(f"CBFError: Comment banned for {reason[1]} seconds. Reason: {reason[2]}")
                return r
        except:
            print("CBFError: Error uploading comment.")

def reply(message, percentage):
    uploadComment(un, pw, message, percentage, lvl)

def read():
    url = f"https://gdbrowser.com/api/comments/{lvl}?count=1"
    r = json.loads(requests.get(url).text)[0]
    com = r['content']
    return com

globals()['reply'] = reply
globals()['read'] = read

helpmsg = "pycbf help\nUsage: pycbf 'script_name.py'\n\nCustom Functions:\n\nread() [used in return to read the comment content]\n\n\nreply(text, percentage) [Comment on the level with a message and a custom percentage]"
try:
    if sys.argv[1] == "--version":
        input("pycbf 1.0 (Python 3.8.0)")
        sys.exit()
    if sys.argv[1] == "--help":
        input(helpmsg)
        sys.exit()
    with open(sys.argv[1], 'r') as py:
        exec(py.read())
except:
    input(helpmsg)
    sys.exit()
