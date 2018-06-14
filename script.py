import sys

class operation:
    op = 0
    values = []
    def __init__(self, op, values):
        self.op = op
        self.values = values
    
    def get(self, delta):
        if self.op <= 7:
            return ("", "+", "-","*", "/", "<<", "I", "R")[self.op] + (" " + str(self.values[0]+delta) if len(self.values) > 0 else "")
        elif self.op == 8:
            return "(" + str(self.values[0]+delta) + " => " + str(self.values[1]+delta) +  ")"
        elif self.op == 9:
            return "SUM "
        elif self.op == 10:
            return "^ " + str(self.values[0]+delta)
        elif self.op == 11:
            return "< "
        elif self.op == 12:
            return "> "
        elif self.op == 13:
            return "|"
        elif self.op == 14:
            return "[+]" + str(self.values[0]) + " "
        elif self.op == 15:
            return "STORE "
        elif self.op == 16:
            return "STORED "
        elif self.op == 17:
            return "LN "

class portal:
    s = 0
    e = 0

    def __init__(self, s, e):
        self.s = s
        self.e = e

op_dict = {
    "+" : 1,
    "-" : 2,
    "*" : 3,
    "/" : 4,
    "<<" : 5,
    "I" : 6,
    "R" : 7,
    "C" : 8,
    "S" : 9,
    "^" : 10,
    "<" : 11,
    ">" : 12,
    "M" : 13,
    "[+]" : 14,
    "ST" : 15,
    "LN": 17,
}
            
opp = []
pts = None
delta = 0
stored = 0
goal = 0
moves = 0
init = 0

def run(o, cur):
    global delta
    global stored
    s = str(cur)
    if o.op == 1:
        return cur+(o.values[0]+delta)
    elif o.op == 2:
        return cur-(o.values[0]+delta)
    elif o.op == 3:
        return cur*(o.values[0]+delta)
    elif o.op == 4:
        return (1<<100) if cur%(o.values[0]+delta) != 0 else cur//(o.values[0]+delta) 
    elif o.op == 5:
        return cur//10
    elif o.op == 6:
        return cur*(10**(len(str(o.values[0]+delta)))) + (o.values[0]+delta)
    elif o.op == 7:
        return int(s[::-1]) if cur >= 0 else -int(str(cur)[1:][::-1])
    elif o.op == 8:
        return int(s.replace(str(o.values[0]+delta), str(o.values[1]+delta)))
    elif o.op == 9:
        return sum(int(x) for x in s) if cur >= 0 else -sum(int(x) for x in s[1:])
    elif o.op == 10:
        return cur**(o.values[0]+delta)
    elif o.op == 11:
        return int(s[1:] + s[0]) if cur >= 0 else -int(s[2:] + s[1])
    elif o.op == 12:
        return int(s[-1]+s[:-1]) if cur >= 0 else -int(s[-1]+s[1:-1])
    elif o.op == 13:
        return int(s + s[::-1]) if cur >= 0 else -int(s[1:]+s[1:][::-1]) 
    elif o.op == 14:
        delta += o.values[0]
        return cur
    elif o.op == 15:
        stored = cur
        return cur
    elif o.op == 16:
        return (1<<100) if stored == 0 else cur*(10**len(str(stored))) + stored
    elif o.op == 17:
        return int(''.join(str(10-int(x) if int(x) != 0 else 0) for x in s)) if cur >= 0 else -int(''.join(str(10-int(x) if int(x) != 0 else 0) for x in s[1:]))

def run_portal(cur):
    s = str(cur)
    l = len(s)
    if pts is None or pts.s > l:
        return cur
    while l >= pts.s:
        cur -= int(s[l-pts.s]) * (10**(pts.s-1))
        cur += int(s[l-pts.s]) * (10**(pts.e-1))
        s = str(cur)
        l = len(s)
        if l > pts.s and s[l-pts.s] == '0':
            cur -= int(s[:-pts.s]) * (10**pts.s)
            cur += int(s[:-pts.s]) * (10**(pts.s-1))
            s = str(cur)
            l = len(s)
    return cur

def solve(cur, ops, dep=0):
    global delta
    global stored
    if len(ops) > 0:
        ops[-1].append(delta)
    if cur > (1<<90) or len(str(cur)) > 6:
        return
    cur = run_portal(cur)
    if cur == goal:
        print(init,end=" ")
        prevstored = -1
        for x in range(len(ops)):
            if ops[x][0].op == 15:
                if prevstored != -1:
                    del ops[prevstored]
                    x -= 1
                prevstored = x
            elif ops[x][0].op == 16:
                prevstored = -1
        for x in ops:
            print(x[0].get(x[1]),end=" ")
        exit(0)
    if dep == moves:
        return
    for x in opp:
        if len(ops) > 0 and ops[-1][0].op == 15 and x.op == 15:
            continue
        ops.append([x])
        curdelta = delta
        curstored = stored
        solve(run(x, cur), ops, dep+(1 if x.op != 15 else 0))
        delta = curdelta
        stored = curstored
        ops.pop()

print("# Moves, Initial Value, Goal")
moves, init, goal = map(int, sys.stdin.readline().split(" "))
for x in op_dict.keys():
    print(x)
print ("\nOperations")
while True:
    p = sys.stdin.readline().strip().split(" ")
    if len(p) == 0 or p[0] == '':
        break
    opp.append(operation(op_dict[p[0].strip()], [int(x) for x in p[1:]]))
    if opp[-1].op == 15:
        opp.append(operation(16, []))
print ("Portal")
p = sys.stdin.readline().strip().split(" ")
if len(p) > 0 and p[0] != '':
    pts = portal(int(p[0]), int(p[1]))

solve(init, [])
print("NOT FOUND")
