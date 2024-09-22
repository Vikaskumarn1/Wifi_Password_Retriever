import subprocess

# getting meta data
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

# decoding meta data
data = meta_data.decode('utf-8', errors="backslashreplace")

# splitting data line by line
data = data.split('\n')

# creating a list of profiles
profiles = []

# traverse the data
for i in data:
    # find "All User Profile" in each item
    if "All User Profile" in i:
        # split the item
        i = i.split(":")
        # item at index 1 will be the Wi-Fi name
        i = i[1]
        # formatting the name (first and last character are useless)
        i = i[1:-1]
        # appending the Wi-Fi name in the list
        profiles.append(i)

# printing heading
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("----------------------------------------------")

# traversing the profiles
for i in profiles:
    # try-catch block begins
    try:
        # getting meta data with password using Wi-Fi name
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
        
        # decoding and splitting data line by line
        results = results.decode('utf-8', errors="backslashreplace")
        results = results.split('\n')

        # finding password from the result list
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

        # if there is password, print the password
        try:
            print("{:<30}| {:<}".format(i, results[0]))

        # else print blank in front of the password
        except IndexError:
            print("{:<30}| {:<}".format(i, ""))
    
    # catch block for subprocess errors
    except subprocess.CalledProcessError:
        print(f"Error retrieving information for {i}")
