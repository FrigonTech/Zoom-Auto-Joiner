import webbrowser
import time
from datetime import datetime
import threading
import json
import os

class MeetingManager:
    def __init__(self):
        self.meetings = []
        self.running = True
        self.load_meetings()

    def load_meetings(self):
        """Load meetings from a JSON file if it exists"""
        if os.path.exists('meetings.json'):
            with open('meetings.json', 'r') as f:
                self.meetings = json.load(f)

    def delete_meetings_temp_file():
        if os.path.exists('meetings.json'):
            os.remove('meetings.json')
            print("Meeting json file deleted successfully!")

    def save_meetings(self):
        """Save meetings to a JSON file"""
        with open('meetings.json', 'w') as f:
            json.dump(self.meetings, f)

    def add_meeting(self, time_str, url):
        """Add a new meeting with validation"""
        try:
            # Validate time format
            datetime.strptime(time_str, "%H:%M")
            self.meetings.append({"time": time_str, "url": url})
            self.save_meetings()
            return True
        except ValueError:
            print("Invalid time format. Please use HH:MM in 24-hour format.")
            return False

    def remove_meeting(self, index):
        """Remove a meeting by index"""
        if 0 <= index < len(self.meetings):
            del self.meetings[index]
            self.save_meetings()
            return True
        return False

    def join_meeting_loop(self):
        """Monitor and join meetings at scheduled times"""
        while self.running:
            current_time = datetime.now().strftime("%H:%M")
            meetings_to_remove = []
            
            for meeting in self.meetings:
                if meeting['time'] == current_time:
                    print(f"\nJoining meeting: {meeting['url']}")
                    try:
                        webbrowser.open(meeting['url'])
                        meetings_to_remove.append(meeting)
                    except Exception as e:
                        print(f"Error joining meeting: {e}")

            # Remove joined meetings
            for meeting in meetings_to_remove:
                self.meetings.remove(meeting)
                self.save_meetings()
            
            time.sleep(1)  # Check every 1 seconds

    def show_menu(self):
        """Display and handle the main menu"""
        while self.running:
            print("\n=== Meeting Auto-joiner Menu ===")
            print("a) Schedule a new meeting")
            print("b) Show all meetings")
            print("c) Remove a meeting")
            print("d) Quit")
            print("e) Remove Meetings.json file")
            
            choice = input("\nEnter your choice: ").lower()

            if choice == 'a':
                time_input = input("Enter time (HH:MM in 24-hour format): ")
                url_input = input("Enter meeting URL: ")
                if self.add_meeting(time_input, url_input):
                    print("Meeting scheduled successfully!")

            elif choice == 'b':
                if not self.meetings:
                    print("No meetings scheduled.")
                else:
                    print("\nScheduled Meetings:")
                    for i, meeting in enumerate(self.meetings):
                        print(f"{i+1}. Time: {meeting['time']} - URL: {meeting['url']}")

            elif choice == 'c':
                if not self.meetings:
                    print("No meetings to remove.")
                else:
                    print("\nCurrent meetings:")
                    for i, meeting in enumerate(self.meetings):
                        print(f"{i+1}. Time: {meeting['time']} - URL: {meeting['url']}")
                    try:
                        index = int(input("Enter the number of the meeting to remove: ")) - 1
                        if self.remove_meeting(index):
                            print("Meeting removed successfully!")
                        else:
                            print("Invalid meeting number.")
                    except ValueError:
                        print("Please enter a valid number.")

            elif choice == 'd':
                self.running = False
                print("Exiting...")
                break
            
            elif choise == 'e':
                delete_meetings_temp_file()

def main():
    manager = MeetingManager()
    
    # Start the meeting monitor in a separate thread
    monitor_thread = threading.Thread(target=manager.join_meeting_loop)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Run the main menu
    manager.show_menu()

if __name__ == "__main__":
    main()
