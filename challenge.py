from dictionaries import seconds


list1 = ["Alex", "Boris", "Chandra"]
list2 = []
for name in list1:
    list2.append(name)

# Create a list of names from the results list

results = [
    ("test_login",    "passed"),
    ("test_cart",     "failed"),
    ("test_checkout", "passed"),
    ("test_logout", "passed"),
]
 
names = []                       # 1. start empty
statuses = []
for name, status in results:     # 2. walk the list
    print(name, status)
    names.append(name)           # 3. put something in
    statuses.append(status)
print(names)

failed_tests = []
for name, status in results:
    if status == "failed":
        failed_tests.append(name)
    elif status == None:
        failed_tests.append(name)

passed_tests = []
for name, status in results:
    if status == "passed":
        failed_tests.append(name)
    elif status == None:
        raise ValueError(f"Test {name} has no status")
    
list3 = [1,2,3,4,5,6,7,8,9,10]

for number in list3:
    if number < 5:
        list3.remove(number)

# Count number of passed tests
passed_tests_count = 0
for name, status in results:
    if status == "passed":
        passed_tests_count += 1
        # passed_tests_count = passed_tests_count + 1

# totalling
durations = [("test_login", "passed", 2.1), ("test_cart", "failed", 0.9)]
total = 0
for name, status, second in durations:
    if status == "passed":
        total = total + seconds



# /////////////////////////////////////////////////////////////////
yesterday = ["test_login", "test_cart", "test_checkout"]
today     = ["test_login", "test_checkout", "test_search"]
 
missing = []                      # which tests disappeared?
for old in yesterday:           #  Loop 1
    found = False
    for new in today:                 #  Loop 2
        if old == new:
            found = True
            break
    if not found:
        missing.append(old)       # ["test_cart"]

same_tests = []
for old in yesterday:
    found = False
    for new in today:
        if old != new:
            found = True
            break
    if not found: 
        same_tests.append(old)

num1 = [1,2,3,4,5]
num2 = [6,2,8,5,5]

greater_than_num2 = []
for num in num1:
    is_greater = False
    for num2 in num2:
        if num > num2:
            is_greater = True
            break
        if not is_greater:
            greater_than_num2.append(num)


if num1 + num2 == 11:   
    if sum(num1) + sum(num2) == 11:
    print("The sum of num1 and num2 is 11")
else:
    print("The sum of num1 and num2 is not 11")


# /////////////////////////////////////////////////////////////////

durations = [
    ("test_login",    2.1),
    ("test_checkout", 8.4),
    ("test_cart",     0.9),
]
 
sorted(durations)                  # sorts by NAME - alphabetical
durations_seconds = []
for name, seconds in durations:
    durations_seconds.append(seconds)

sorted(durations, key=durations_seconds) # sorts by TIME
