# read in  message.txt as a string
with open("message.txt", "r") as f:
    message = f.read()

# loop through each character in the message and find
# when the last 14 characters are all different. Set
# the index of the current character to marker_index.
marker_index = 0
for i in range(13, len(message)):
    # select the last 14 characters
    last14 = message[i - 14 : i]
    # check if they are all different
    if len(set(last14)) == 14:
        marker_index = i
        break

# print the marker_index
print(marker_index)
