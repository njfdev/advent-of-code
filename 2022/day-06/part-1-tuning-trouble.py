# read in  message.txt as a string
with open("message.txt", "r") as f:
    message = f.read()

# loop through each character in the message and find
# when the last 4 characters are all different. Set
# the index of the current character to marker_index.
marker_index = 0
for i in range(3, len(message)):
    # select the last 4 characters
    last4 = message[i - 4 : i]
    # check if they are all different
    if len(set(last4)) == 4:
        marker_index = i
        break

# print the marker_index
print(marker_index)
