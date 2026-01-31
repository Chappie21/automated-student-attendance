from model.geminiAdapter import GeminiAdapter
from dotenv import load_dotenv
from utils.menu import AttendanceUI
from utils.attendance_runner import run_attendance_flow
import os

load_dotenv()

def main():
    ui = AttendanceUI()
    
    client = GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL")
    )

    # read prompt from prompt.txt
    with open("prompt.txt", "r", encoding="utf-8") as f:
        textPrompt = f.read().strip()

    if not textPrompt:
        ui.show_error("The prompt is empty. Please provide a valid prompt in prompt.txt")
        return

    choice = 0

    while (choice != 4):
        ui.clean_console()

        ui.display_header()
        choice = ui.main_menu()

        # clear console
        ui.clean_console()

        # Handle menu choices
        if choice == 1:
            run_attendance_flow(ui, client, textPrompt)
        elif choice == 2:
            ui.show_info("Mark attendance in Google Sheets feature is coming soon!")
        elif choice == 3:
            ui.help_menu()

        if choice != 4:
            # press enter to continue
            ui.show_info("Press Enter to return to the main menu...")
            input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")