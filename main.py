from model.geminiAdapter import GeminiAdapter
from model.sheetsAdapter import SheetsAdapter
from dotenv import load_dotenv
from utils.menu import AttendanceUI
from utils.attendanceRunner import run_attendance_flow, mark_student_attendance
import os

load_dotenv()

def main():
    ui = AttendanceUI()
    
    client = GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL")
    )

    sheet = SheetsAdapter(
        creds_json_path=os.getenv("GOOGLE_CREDS_JSON_PATH"),
        spreadsheet_key=os.getenv("GOOGLE_SPREADSHEET_KEY")
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
            run_attendance_flow(ui, client, sheet, textPrompt)

        elif choice == 2:
            mark_student_attendance(sheet, ui)

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