
command = ["up", "down", "left", "right", "a", "b", "enter", "select", "l", "r"]
cmd = "upupgupupupdowndowndown"

tmp = [0 for i in range(len(command))]


while cmd:
    flag = False
    for i in range(len(command)):
        count = 0
        while cmd[:len(command[i])] == command[i]:
            flag = True
            cmd = cmd[len(command[i]):]
            count += 1
        tmp[i] = max(tmp[i], count)
    if not flag: cmd = cmd[1:]

remain_cmd = []
max_value = 0
for i in range(len(command)):
    if tmp[i] == max_value:
        remain_cmd.append(command[i])
    elif tmp[i] > max_value:
        max_value = tmp[i]
        remain_cmd = [command[i]]

print(tmp)
print(remain_cmd)
