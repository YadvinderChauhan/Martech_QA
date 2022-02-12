
# Health Management System
# Total 6 Files, 3 For exercise and 3 For for diet
# 3 clients - Harry, Rohan and Hammad
# write a function that when executed takes as input client name
# one more function to retrieve exercise or food for any client
import datetime

clients = {1: "Harry", 2: "Rohan", 3: "Hammad"}

def getdate():
    import datetime
    return datetime.datetime.now()

print("This is a Health Management System.\nYou can find out about the excercise or the diet of you client.")
user_option = int(input("\nPlease select a client by entering\n1 for Harry\n2 for Rohan\n3 for Hammad\nPlease make your selection now: "))

while user_option not in clients:
    print("Incorrcet option. Client doesn't exist")
    user_option = int(input("\nPlease select from the given options only: "))
    if user_option in clients:
        client_option = int(input("\nPlease select 1 for Diet and 2 for Excercise: "))
