report = {
    "run": 42,
    "branch": "master",
    "tests": [
        {"name": "test_login",  "file": "test_login.py",   "status": "passed",  "seconds": 2.1},
        {"name": "test_locked", "file": "test_login.py",   "status": "failed",  "seconds": 0.8},
        {"name": "test_add",    "file": "test_cart.py",    "status": "passed",  "seconds": 1.4},
        {"name": "test_remove", "file": "test_cart.py",    "status": "passed",  "seconds": 1.1},
        {"name": "test_create", "file": "test_booking.py", "status": "passed",  "seconds": 0.3},
        {"name": "test_delete", "file": "test_booking.py", "status": "failed",  "seconds": 0.4},
        {"name": "test_update", "file": "test_booking.py", "status": "skipped", "seconds": 0.0},
    ],
}

statuses = {}

for test in report["tests"]:
    #                  test_login -> passed
    if test["status"] == "passed":
        statuses[test["name"]] = test["status"]


seconds = 0

for test in report["tests"]:
    seconds += test["seconds"]


count = {}

for test in report["tests"]:
    count[test["status"]] = (count.get(test["status"], 0) + 1)
  
print(count)

files = set()

for test in report["tests"]:
    files.add(test["file"])

new_dict = dict.fromkeys(files)

print(count)

files_used = set()

for test in report["tests"]:
    files_used.add(test["file"])

new_dict = dict.fromkeys(files)

# failes names
failed_names = []

for test in report["tests"]:
    if test["status"] == "failed":
        failed_names.append(test["name"])

#2 status_lookup
status_lookup = {}

for test in report["tests"]:
    status_lookup[test["name"]] = test["status"]

#3 count bu status
count_by_status = {}

for test in report["tests"]:
    count_by_status[test["status"]] = count_by_status.get(test["status"], 0) + 1

#4 files used

for test in report["tests"]:
    files_used.add(test["file"])


# 1 - failed_names(report) → the names that failed. Walk the list.
# 2 - status_lookup(report) → {name: status}. Build a dictionary.
# 3 - count_by_status(report) → {"passed": 4, "failed": 2, "skipped": 1}. Count
# 4 - files_used(report) → the three filenames, once each. Use a set.
