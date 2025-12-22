from flask import Flask,render_template,request,redirect
import random,hashlib,secrets
from flask import session
app=Flask(__name__)
app.secret_key = secrets.token_hex(32)
global_lib={}
mem=""
sandboxes={}
sidname={}
T2TOS_COMMANDS = [
    "/help","/chat.clean","/chat.clear","/userbuf.clear","/plus","/min","/mul","/div","/mod","/chat.len",
    "/file.save","/file.open","/file.delete","/file.deleteall","/exit","/echo","/lib.all",
    "/pow","/hello","/item","/ask","/pi","/space","/joke","/file.copy","/theme.black","/theme.hacker","in","/theme.cyberpunk","/theme.forest","/theme.sunset","/theme.ocean","/theme.retro","/theme.pastel","/theme.galaxy","/theme.matrix","/theme.sunrise","/theme.twilight","/theme.cyberforest","/lib.get","/lib.save",
    "/try","/for","/thread","/range","/file.all","/desktop","/theme.","/mode.v2","/mode.v1","/theme.light","/theme.red-light","/theme.blue","/theme.light-red","/theme.red","/theme.dark","/theme.vscode","/theme.vscode-hc","/theme.pycharm","/q","/theme.BLACK"
]
userspasswords={}
def ip():
    if "sid" not in session:
        session["sid"] = secrets.token_hex(16)
    return session["sid"]
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()
@app.template_filter('highlight_t2tos')
def highlight_t2tos(text):
    import re
    from markupsafe import Markup

    tokens = re.split(r'(\s+|[\[\]\(\)\{\}\$%;,@#|<>&]|\=| |com/|sys/|txt/|var/|lst/|lib/|fnc/)', text)
    result = []
    i=0
    for t in tokens:
        try:
            isvar=(tokens[i-1]=="<"and tokens[i+1]==">") or (tokens[i-1]=="$" and tokens[i+1]=="$")or (tokens[i-1]=="$" and tokens[i+1]=="=") or t=="$" or t=="=" or t=="<" or t==">"
        except:
            isvar=False
        if not t or t.isspace():
            result.append(t)
        elif t.strip() in T2TOS_COMMANDS:
            result.append(f'<span class="t2tos-command">{t}</span>')
        elif isvar:
            result.append(f'<span class="t2tos-var">{t}</span>')
        elif t.strip().isdigit():
            result.append(f'<span class="t2tos-number">{t}</span>')
        elif t in [';', '|', '@', "]","}",")","{","[","(","%","&","#"]:
            result.append(f'<span class="t2tos-symbol">{t}</span>')
        elif t in ['random', 'chat', '>'] and tokens[i-1]=="<":
            result.append(f'<span class="t2tos-command">{t}</span>')
        elif t in ["com/","sys/","txt/","var/","lst/","fnc/","lib/"]:
            result.append(f'<span class="t2tos-fileext">{t}</span>')
        else:
            # Keep everything else plain (for rendering to work)
            result.append(t)
        i+=1
    
    return Markup(''.join(result))
app.jinja_env.filters['highlight_t2tos'] = highlight_t2tos
############################################################
#                          CLASSES                         #
############################################################
class SandBox:
    __slots__=('__chat', '__files','__theme','__mode','__history','__usersees')
    def __init__(self):
        self.__chat=[""]*40
        self.__files={}
        self.__mode="v1"
        self.__theme="dark"
        self.__history = []
        self.__usersees=[""]*40
    @property
    def chat(self):
        return self.__usersees
    @property
    def theme(self):
        return self.__theme
    @property
    def history(self):
        return self.__history
    def safeCommand(self,com:str):
            self.__chat.pop(0)
            self.__chat.append(com)
            self.__usersees.pop(0)
            self.__usersees.append(com)
            if com.strip():
                self.__history.append(com)
                self.__history = self.__history[-200:]
            if len(com)>0 and "import" not in str(com):
                def checkcommand(a:str,/,userss=False):
                    print(f"{ip()} - checkcommand - {a}")
                    QUOTES = [
                        "The best way to predict the future is to invent it. – Alan Kay",
                        "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
                        "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
                        "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
                        "Imagination is more important than knowledge. – Albert Einstein",
                        "Happiness is not something ready made. It comes from your own actions. – Dalai Lama",
                        "Everything you’ve ever wanted is on the other side of fear. – George Addair",
                        "Do what you can, with what you have, where you are. – Theodore Roosevelt",
                        "It always seems impossible until it’s done. – Nelson Mandela",
                        "Act as if what you do makes a difference. It does. – William James"
                    ]
                    ALLOWED_PREFIXES = ("/", "$", "@")
                    if not com.startswith(ALLOWED_PREFIXES):
                        raise SystemError("Sandbox: invalid command")
                    a=a.replace("${in}","<chat -2>")
                    import re
                    def REplaceall(source:str,n1,n2):
                        patternn = re.compile(n1, re.DOTALL)
                        source = re.sub(source,patternn, str(n2))
                        return source
                    def REplace1(source:str,n1,n2):
                        patternn = re.compile(n1, re.DOTALL)
                        source = re.sub(patternn, str(n2), source,count=1)
                        return source
                    def RE(source:str, pr: dict):
                        for pattern in pr:
                            patternn = re.compile(pattern, re.DOTALL)
                            source = re.sub(patternn, str(pr[pattern]), source)
                        return source
                    def REfindall(source:str, pattern):
                        patternn = re.compile(pattern, re.DOTALL)
                        source = re.findall(patternn, source)
                        return source
                    if "/file.save[com/" not in a and "/file.save[sys/" not in a:
                        for i in REfindall(a, r"<random -?\d+ -?\d+>"):
                            t=random.randint(int(i.split()[1]),int(i.split()[2][:-1]))
                            a=REplace1(a,i,t)
                    if "/file.save[com/" not in a and "/file.save[sys/" not in a:
                        for i in REfindall(a, r"<chat -?\d+>"):
                            t=self.__chat[int(i.split()[1][:-1])]
                            a=REplace1(a,i,t)
                    if "/file.save[com/" not in a and "/file.save[sys/" not in a:
                        for i in REfindall(a, r"<history -?\d+>"):
                            t=self.__history[int(i.split()[1][:-1])]
                            a=REplace1(a,i,t)
                    def types(file:str):
                        if file not in self.__files:
                            return "[###/]:"+file
                        else:
                            match self.__files[file][:4]:
                                case "lst/":
                                    return "[lst/]:"+file
                                case "var/":
                                    return "[var/]:"+file
                                case "sys/":
                                    return "[sys/]:"+file
                                case "com/":
                                    return "[com/]:"+file
                                case "txt/":
                                    return "[txt/]:"+file
                                case "lib/":
                                    return "[lib/]:"+file
                                case "fnc/":
                                    return "[fnc/]:"+file
                                case _:
                                    return "[    ]:"+file
                    def typeWithoutfile(file:str):
                        if file not in self.__files:
                            return ""
                        else:
                            match self.__files[file][:4]:
                                case "lst/":
                                    return "lst/"
                                case "var/":
                                    return "var/"
                                case "sys/":
                                    return "sys/"
                                case "com/":
                                    return "com/"
                                case "txt/":
                                    return "txt/"
                                case "lib/":
                                    return "lib/"
                                case "fnc/":
                                    return "fnc/"
                                case _:
                                    return ""
                    v12v2={"try":"/try","for":"/for","thread":"/thread"}
                    if self.__mode=="v1":
                        for i in v12v2:
                            a=a.replace(v12v2[i],"")
                        for i in v12v2:
                            a=a.replace(i,v12v2[i])
                    for i in self.__files:
                        if types(i)[2]!=" ":
                            a=str(a).replace(f"<{i}>",str(self.__files[i][4:]))
                        else:
                            a=str(a).replace(f"<{i}>",str(self.__files[i]))
                    def addtochat(text:str):
                        print(f"{ip()} - addtochat - {text}")
                        self.__chat.pop(0)
                        self.__chat.append(str(text))
                    def say(text:str):
                        print(f"{ip()} - say - {text}")
                        self.__usersees.pop(0)
                        self.__usersees.append(str(text))
                    if userss:
                        def addtochat(text:str):
                            say(text)
                            self.__chat.append(text)
                            self.__chat.pop(0)
                    if len(a)>0:
                        for i in self.__files:
                            if self.__files[i][:4]=="var/":
                                a=str(a).replace(f"<{i}>",str(self.__files[i][4:]))
                        if a=="/chat.clean" or a=="/chat.clear":
                            self.__chat=[""]*40
                        elif a=="/mode.v2":
                            addtochat("this is an experemental extention for T2TOS")
                            self.__mode="v2"
                        elif a=="/mode.v1":
                            self.__mode="v1" 
                        elif a=="/help":
                            say(" | ".join(T2TOS_COMMANDS))
                        elif a.startswith("/theme."):
                            self.__theme=a.removeprefix("/theme.")
                        elif a=="/quote":
                            addtochat(random.choice(QUOTES))
                        elif a[:5]=="/plus":
                            addtochat(int(a[6:].split()[0])+int(a[6:].split()[1]))
                        elif a[:5]=="/userbuf.clear":
                            self.__usersees=[""]*40
                        elif a[:3]=="/sum":
                            addtochat(sum([int(i) for i in a[6:].split()]))
                        elif a[:5]=="/echo":
                            say(a[6:])
                            addtochat(a[6:])
                        elif a[:2] == "/q":
                            checkcommand(a[3:],userss=True)
                        elif a[:8] == "/lib.get":
                            self.__files.setdefault(a[9:],global_lib[a[9:]])
                            checkcommand(f"@{a[9:]}")
                        elif a[:8] == "/lib.all":
                            for i in global_lib:
                                addtochat(i)
                                say(i)
                        elif a[:4]=="/min":
                            addtochat(int(a[5:].split()[0])-int(a[5:].split()[1]))
                        elif a[:4]=="/mul":
                            addtochat(int(a[5:].split()[0])*int(a[5:].split()[1]))
                        elif a[:4]=="/div":
                            addtochat(int(a[5:].split()[0])/int(a[5:].split()[1]))
                        elif a[:4]=="/mod":
                            addtochat(int(a[5:].split()[0])%int(a[5:].split()[1]))
                        elif a=="/chat.len":
                            addtochat(len(self.__chat))
                        elif a[0]=="$" and a.count("$")>=2:
                            s=a.split("$")
                            if s[1] in self.__files.keys() and self.__files[s[1]][:4]=="var/":
                                self.__files[s[1]]="var/"+"$".join(s[2:])
                            else:
                                self.__files.setdefault(s[1],"var/"+"$".join(s[2:]))
                            addtochat(self.__chat[-2])
                        elif a[:10]=="/lib.save[":
                            if a[10:].split("]")[0][:4]=="lib/":
                                s=a[10:].split("]")
                                global_lib.setdefault(s[1],s[0])
                        elif a[:11]=="/file.save[":
                            s=a[11:].split("]")
                            self.__files.setdefault("]".join(s[1:]),s[0])
                        elif a[:11]=="/file.save(":
                            s=a[11:].split(")")
                            self.__files.setdefault(")".join(s[1:]),s[0])
                        elif a[:11]=="/file.save{":
                            s=a[11:].split("}")
                            self.__files.setdefault("{".join(s[1:]),s[0])
                        elif a[:11]=="/file.open ":
                                if self.__files[a[11:]][:4]=="lst/":
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="lst/":
                                            addtochat(types(i[4:]))
                                        else:
                                            addtochat(types(i))
                                elif self.__files[a[11:]][:4]=="com/":
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="com/":
                                            addtochat(i[4:])
                                            checkcommand(i[4:])
                                        else:
                                            addtochat(i)
                                            checkcommand(i)
                                elif self.__files[a[11:]][:4]=="fnc/":
                                    file:str=self.__files[a[11:]]
                                    for i in range(len(self.__chat[-1].split(" "))):
                                        file=file.replace("${"+str(i)+"}",self.__chat[-1].split(" ")[i]);print(1)
                                    for i in file.split(";"):
                                        if i[:4]=="fnc/":
                                            addtochat(i[4:])
                                            checkcommand(i[4:])
                                        else:
                                            print(i)
                                            addtochat(i)
                                            checkcommand(i)
                                elif self.__files[a[11:]][:4]=="lib/":
                                    for i in self.__files[a[11:]].split("#")[-1].split("&"):
                                            checkcommand(f"/file.save[{i.split("%")[1]}]{i.split("%")[0]}")
                                elif self.__files[a[11:]][:4]=="sys/":
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="sys/":
                                            if i[4:]!="":
                                                addtochat(i[4:]+str(self.__chat[-1]))
                                                checkcommand(i[4:]+str(self.__chat[-2]))
                                            else:
                                                addtochat("")
                                        else:
                                            if i!="":
                                                addtochat(i+str(self.__chat[-1]))
                                                checkcommand(i+str(self.__chat[-2]))
                                            else:
                                                addtochat("")
                                elif self.__files[a[11:]][:4]=="var/":
                                    addtochat(self.__files[a[11:]][4:])
                                elif self.__files[a[11:]][:4]=="txt/":
                                    addtochat(self.__files[a[11:]][4:])
                                else:
                                    addtochat(self.__files[a[11:]])
                        elif a[:10]=="/file.text":
                            addtochat("["+self.__files[a[11:]]+"]")
                        elif a[:10]=="/file.test":
                                if self.__files[a[11:]][:4]=="lst/":
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="lst/":
                                            say(types(i[4:]))
                                        else:
                                            say(types(i))
                                elif self.__files[a[11:]][:4]=="com/":
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="com/":
                                            say(i[4:])
                                        else:
                                            say(i)
                                elif self.__files[a[11:]][:4]=="sys/":
                                    addtochat("/in/")
                                    for i in self.__files[a[11:]].split(";"):
                                        if i[:4]=="sys/":
                                            if i[4:]!="":
                                                addtochat(i[4:]+str(self.__chat[-1]))
                                                say(i[4:]+str(self.__chat[-1]))
                                            else:
                                                addtochat("")
                                        else:
                                            if i!="":
                                                say(i+str(self.__chat[-1]))
                                                addtochat(i+str(self.__chat[-1]))
                                            else:
                                                addtochat("")
                                elif self.__files[a[11:]][:4]=="var/":
                                    addtochat(self.__files[a[11:]][4:])
                                elif self.__files[a[11:]][:4]=="txt/":
                                    addtochat(self.__files[a[11:]][4:])
                                else:
                                    addtochat(self.__files[a[11:]])
                        elif a=="/exit":
                            raise Exception("/exit")
                        elif a[:13]=="/file.delete ":
                            del self.__files[a[13:]]
                        elif a=="/file.deleteall":
                            self.__files={}
                            addtochat("deleted files"+str(self.__files))
                            self.__files={}
                        elif a[:4]=="/pow":
                            addtochat(str(int(a[5:].split()[0])**int(a[5:].split()[1])))
                        elif a[:6]=="/hello":
                            addtochat(f"Hello {a[7:]}!")
                            say(f"Hello {a[7:]}!")
                        elif a[:5]=="/item":
                            addtochat(self.__chat.index(a[6:]))
                        elif a[:4]=="/ask":
                            say(f"{a[5:]}?")
                        elif a=="/pi":
                            addtochat("3.1415926535897")
                        elif a[:6]=="/space":
                            for i in range(int(a[7:])):
                                addtochat(" ")
                        elif a[:5]=="/joke":
                            for i in range(int(a[6:])):
                                say("кабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачоккабачок")
                        elif a[:7]=="/mem.in":
                            mem=a[8:]
                        elif a=="/mem.out":
                            addtochat(mem)
                        elif a=="/chat.2rlast":
                            self.__chat=["",""]+self.__chat[:-3]
                        elif a=="/chat.3rlast":
                            self.__chat=["","",""]+self.__chat[:-3]
                        elif a=="/chat.rlast":
                            self.__chat=[""]+self.__chat[:-2]
                        elif a=="/file.all":
                            for i in self.__files:
                                addtochat(types(str(i)))
                                say(types(str(i)))
                        elif a=="/desktop":
                            for i in self.__files:
                                if not( (f";{i};" in "|".join(list(self.__files.values()))or f";{i}|" in "|".join(list(self.__files.values()))) or (f"/{i};" in "|".join(list(self.__files.values())) or f"/{i}|" in "|".join(list(self.__files.values()))) ):
                                    addtochat(types(str(i)))
                                    say(types(str(i)))
                        elif a[:11]=="/file.copy(":
                            s=a[11:].split(")")
                            self.__files.setdefault(s[1],self.__files[s[0]])
                        elif a[:11]=="/file.copy[":
                            s=a[11:].split("]")
                            self.__files.setdefault(s[1],self.__files[s[0]])
                        elif a[:11]=="/file.copy{":
                            s=a[11:].split("}")
                            self.__files.setdefault(s[1],self.__files[s[0]])
                        elif a[:11]=="/file.name(":
                            s=a[11:].split(")")
                            checkcommand(f"/file.copy({s[0]}){")".join(s[1:])}")
                            checkcommand(f"/file.delete {s[0]}")
                        elif a[:6]=="/split":
                            s=a[7:].split(" ")
                            addtochat(s[0].split(s[1])[int(s[2])])
                        elif a[:4]=="/try":
                            try:
                                checkcommand(a[5:])
                            except Exception as e:
                                print(repr(e))
                                addtochat(repr(e))
                        elif a[:4]=="/if " and self.__mode=="v2":
                            sp=a[5:]
                            i1="N"*6+sp
                            if i1[6:].split(":")[1]=="=":
                                if i1[6:].split(":")[0]==i1[6:].split(":")[2][:-1]:
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                            if i1[6:].split(":")[1]=="!=":
                                if i1[6:].split(":")[0]!=i1[6:].split(":")[2][:-1]:
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                            if i1[6:].split(":")[1]==">":
                                if int(i1[6:].split(":")[0])>int(i1[6:].split(":")[2][:-1]):
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                            if i1[6:].split(":")[1]=="<":
                                if int(i1[6:].split(":")[0])<int(i1[6:].split(":")[2][:-1]):
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                            if i1[6:].split(":")[1]==">=":
                                if int(i1[6:].split(":")[0])>=int(i1[6:].split(":")[2][:-1]):
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                            if i1[6:].split(":")[1]=="<=":
                                if int(i1[6:].split(":")[0])<=int(i1[6:].split(":")[2][:-1]):
                                    checkcommand(":".join(i1[6:].split(":")[3:]))
                        elif a[:4]=="/for" and a[5:].split(" ")[1]=="in":
                            s=a[5:].split(" ")
                            for i in range(int(s[2])):
                                s1=str(" ".join(s[3:])).replace(f"<{s[0]}>",str(i))
                                if not( s1[:3]=="for" and s1[4:].split(" ")[1]=="in"):
                                    addtochat(s1)
                                checkcommand(s1)
                        elif a[:6]=="/range":
                            addtochat(";".join(list(range(a[7:]))))
                        elif a[0]=="@":
                            if types(a[1:].split(" ")[0])[2]=="y" or types(a[1:].split(" ")[0])[2]=="n":
                                addtochat(" ".join(a[1:].split(" ")[1:]))
                                checkcommand(f"/file.open {a[1:].split(" ")[0]}")
                            else:
                                checkcommand(f"/file.open {a[1:].split(" ")[0]}")
                        if a[0]=="$"and "=" in a:
                            addtochat(a.split("=")[1])
                            checkcommand(a.split("=")[1])
                            if a.split("=")[0][1:] not in self.__files:
                                self.__files.setdefault(a.split("=")[0][1:],"")
                            self.__files[a.split("=")[0][1:]]=typeWithoutfile(a.split("=")[0][1:])+self.__chat[-1]
                checkcommand(com)
                return True
############################################################
#                          T2TOS                           #
############################################################
@app.route('/T2TOS/login')
def a291():
    return render_template("auth.html",)
@app.route('/T2TOS/login/done',methods=["POST"])
def a292():
    name = request.form.get("user", "")
    p = request.form.get("pass", "")
    if (name in userspasswords and p == userspasswords[name]) or name not in userspasswords:
        userspasswords.setdefault(name,p)
        sidname.setdefault(ip(),name)
        sandboxes.setdefault(name,SandBox())
        return redirect("/T2TOS")
    else:
        return redirect("/T2TOS/login")
@app.route('/')
def a292():
    return redirect("/T2TOS")

@app.route('/T2TOS/exception')
def a293():
    if ip() not in sidname:
        return redirect("/T2TOS/login")
    return render_template("button.html",text="Your T2TOS run into a problem :(",button_name="back",button_href="/T2TOS")
@app.route('/T2TOS')
def a20():
    if ip() not in sidname:
        return redirect("/T2TOS/login")
    return render_template("list.html",theme=sandboxes[sidname[ip()]].theme,chat=sandboxes[sidname[ip()]].chat,title=f"{sidname[ip()]}'s T2TOS",text=f"{sidname[ip()]}'s T2TOS")
@app.route("/redir", methods=["POST","GET"])
def check_page():
    try:
        p = request.form.get("command", "")
        sandboxes[sidname[ip()]].safeCommand(p)
    except:
        return redirect("/T2TOS/exception")
    return redirect("/T2TOS")
