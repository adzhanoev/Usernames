import time, requests, math, concurrent.futures as cf
 
start_time = time.time()
 
f = open("usernames.txt", "a")
 
CONNECTIONS = 20
 
def get_usernames():
    my_list = list()
 
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890-_"
 
    a = alphabet[0:26] # letters
    b = alphabet[36:] # dash and underscore
    c = alphabet[26:36] # numbers
    
    for l1 in alphabet[14:]: # opqrstuvwxyz1234567890-_
        for l2 in alphabet:
            for l3 in alphabet:
 
                condition1 = l1 in a and l2 in a and l3 in a
                condition2 = l1 in b and l2 in b and l3 in b
                condition3 = l1 in c and l2 in c and l3 in c
 
                if not condition1 and not condition2 and not condition3:
                    my_list.append(l1 + l2 + l3)
    return my_list
 
def check_username(username):
    r = requests.get(f"https://api.scratch.mit.edu/accounts/checkusername/{username}/")
    good_response = '{"username":"' + username + '","msg":"valid username"}'
    return r.text == good_response # example good response: {"username":"InsertUsernameHere","msg":"valid username"}
 
def write_to_file(list):
    for item in list[0:-1]:
        f.write(item.upper() + "\n")
    f.write(list[-1].upper())
 
def round_to_the_nearest_ten(n):
    return int(math.ceil(n / 10.0)) * 10
 
usernames = get_usernames()
 
available_usernames = list()
combinations = round_to_the_nearest_ten(len(usernames)) # it's 25536 but we round it up to 25540 because we can divide 25540 by 10
 
counter = 0
with cf.ThreadPoolExecutor(max_workers = CONNECTIONS) as executor:
    future_to_url = {executor.submit(check_username, username): username for username in usernames}
    for future in cf.as_completed(future_to_url):
 
        counter += 1
        if counter % (combinations / 10) == 0.0:
            print(str(int((counter / combinations) * 100)) + " % Done")
 
        username = future_to_url[future]
        if future.result():
            available_usernames.append(username)
 
print("100 % Done")
 
available_usernames = sorted(available_usernames, key = lambda src: ["abcdefghijklmnopqrstuvwxyz1234567890-_".index(char) for char in src])
 
f.truncate(0) # clear file contents
write_to_file(available_usernames)
f.close()
 
print("\n" + "Execution Time: " + str(round(((time.time() - start_time)/60), 3)) + " Minutes")
