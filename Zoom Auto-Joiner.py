import webbrowser
import schedule
import time
import threading
from datetime import datetime

# Defining format and marking this out in the scheduler by enumerating this list
meetings = [{"time": "00:00", "url": "link"}]

def join_meeting(meeting_url):
    
    print(f"Joining meeting: {meeting_url}")
    webbrowser.open(meeting_url)

def schedule_auto_join_meeting():
    for index, meeting in enumerate(meetings):
        if index == 0:
            continue
        schedule_time = meeting["time"]
        print(f"Scheduling meeting at {schedule_time} with URL: {meeting['url']}")
        schedule.every().day.at(schedule_time).do(lambda m=meeting["url"]: join_meeting(m))
        print(f"Scheduled meeting at {schedule_time} for today")

# Run scheduled tasks
def run_scheduler():
    while True:
        current_time = datetime.now().strftime("%H:%M")
        #print(f"Current time: {current_time}")
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

def show_menu():
    while True:
        print("What do you want to do?: \na) Schedule a meeting to auto join \nb) Quit \nc) Restart \nd) Launch demo website \ne) Show Meetings \n")
        str1 = input()

        if str1 == "a":
            str2 = input("Enter Hours and Minutes in hh:mm format (e.g., 14:30) in 24-hour form: \n")
            if str2=="restart":
                continue
            str3 = input("Enter meeting link: \n")
            if str3=="restart":
                continue
            meetings.append({"time": f"{str2}", "url": f"{str3}"})
            print("Meetings: ", meetings)
            schedule_auto_join_meeting()
        elif str1 == "b":
            print("Exiting the menu...")
            break
        elif str1 == "c":
            continue
        elif str1 == "d":
            join_meeting("https://www.google.com")
        elif str1 == "e":
            print(meetings)
        else:
            print("Invalid option, please try again.")
            continue

# Run the menu function
menu_thread = threading.Thread(target=show_menu)
menu_thread.daemon = True
menu_thread.start()

# Keep the main thread alive
while True:
    time.sleep(1)
