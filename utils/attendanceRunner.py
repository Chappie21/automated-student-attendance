from model.geminiAdapter import GeminiAdapter
from model.sheetsAdapter import SheetsAdapter
from utils.menu import AttendanceUI
from utils.converter import convertToList
from datetime import datetime
import os

def run_attendance_flow(ui: AttendanceUI, client: GeminiAdapter, sheet: SheetsAdapter, text_prompt: str):
    """
        Run the interactive attendance loop. This function contains the same
        logic previously in `main.py` and was extracted here to keep the main
        module focused on wiring.

        Parameters:
        - ui: AttendanceUI instance
        - client: GeminiAdapter instance
        - sheet: SheetsAdapter instance
        - text_prompt: prompt text (string)
    """

    # Search for photo and evaluate attendance
    while True:
        image_path = ui.request_input("Please provide the path to the image file:", "Path: ")

        if os.path.isfile(image_path):
            break
        else:
            ui.show_error(f"The file '{image_path}' does not exist. Please try again.")

    ui.clean_console()

    # Request seccion and date
    seccion = ui.request_input("Please provide the section name (worksheet name in Google Sheets):", "Section: ")
    date = ui.request_input("Please provide the date for marking attendance (YYYY-MM-DD) or leave blank for today:", "Date (optional): ")

    ui.clean_console()

    ui.start_loading("Analyzing image with Gemini API")
    try:
        # Get analaysis of the image from Gemini
        response = client.generate_from_image(image_path, prompt=text_prompt)

        # parse response to list of dicts
        response_dict = convertToList(response)
    except Exception as e:
        ui.show_error(f"Failed to communicate with Gemini: {e}")
        raise

    ui.stop_loading()
    ui.show_success("Image processed successfully!")

    ui.start_loading("Connecting to Google Sheets and marking attendance")
    try:
        # Create a new column with the date of today if not exists
        worksheet_name = seccion
        worksheet = sheet.get_worksheet(worksheet_name)

        ui.show_success(f"Connected to worksheet: {worksheet_name} successfully!")

        # Get all headers
        headers = worksheet.row_values(1)

        # Get today's date or use provided date
        today = date if date else datetime.now().strftime("%Y-%m-%d")

        # Check if today's date column exists
        if today not in headers:
            col_index = len(headers) + 1

            # insert_cols add a new column at the end with today's date as header
            worksheet.insert_cols([[today]], col=col_index, inherit_from_before=True)
            worksheet.update_cell(1, col_index, today)
        else:
            # If it already exists, we look for the column number so we can use it later.
            col_index = headers.index(today) + 1

        # Verify that the ID matches the correct row and mark attendance in the created/existing column.
        for record in response_dict:
            student_id = record.get("id") or record.get("ID") or record.get("Id")

            ui.update_loading(f"Marking attendance for ID {student_id}")

            if not student_id:
                continue

            try:
                cell = worksheet.find(str(student_id))
                row_number = cell.row
                ui.update_loading(f"Marking attendance for ID {student_id}")

                # Marcar asistencia con "P" (Presente)
                worksheet.update_cell(row_number, col_index, "P")
            except Exception as e:
                ui.show_error(f"ID {student_id} not found in worksheet '{worksheet_name}'.")

        # Set absences for those not marked present
        all_ids = [str(record.get("id") or record.get("ID") or record.get("Id")) for record in response_dict]
        id_cells = worksheet.col_values(1)[1:]  # exclude header
        for idx, student_id in enumerate(id_cells, start=2):  # start=2 to account for header row
            if student_id not in all_ids:
                ui.update_loading(f"Marking absence for ID {student_id}")
                worksheet.update_cell(idx, col_index, "A")

    except Exception as e:
        ui.show_error(f"Failed to mark attendance in Google Sheets: {e}")
        raise

    ui.stop_loading()
    ui.show_success("Attendance marked successfully!")


def mark_student_attendance(sheet: SheetsAdapter, ui: AttendanceUI):
    """
        Mark attendance for a single student in the worksheet.

        Parameters:
        - sheet: SheetsAdapter instance
        - ui: AttendanceUI instance
    """
    try:
        # Request section and date
        seccion = ui.request_input("Please provide the section name (worksheet name in Google Sheets):", "Section: ")
        
        ui.start_loading(f"Connecting to worksheet: {seccion}")
        worksheet = sheet.get_worksheet(seccion)
        ui.stop_loading()
        ui.show_success(f"Connected to worksheet: {seccion} successfully!")

        student_id = ui.request_input("Enter the student ID to mark attendance for:", "Student ID: ")

        cell = worksheet.find(str(student_id))
        row_number = cell.row

        # request date column (today by default) and mark attendance with "P" (Present) or "A" (Absent)
        cDate = ui.request_input("Enter the date for marking attendance (YYYY-MM-DD) or leave blank for today:", "Date (optional): ")

        if not cDate:
            cDate = datetime.now().strftime("%Y-%m-%d")

        # Check if the date column exists, if not create it
        headers = worksheet.row_values(1)

        if cDate not in headers:
            new_col_index = len(headers) + 1
            worksheet.insert_cols([[cDate]], col=new_col_index, inherit_from_before=True)
            worksheet.update_cell(1, new_col_index, cDate)
            col_index = new_col_index
        else:
            col_index = headers.index(cDate) + 1

        status = ui.request_input("Enter attendance status (P for Present, A for Absent):", "Status (P/A): ").upper()

        ui.start_loading(f"Marking attendance for ID {student_id}")

        # Mark attendance with "P" (Present) or "A" (Absent)
        worksheet.update_cell(row_number, col_index, status)
        ui.stop_loading()

        ui.show_success(f"Attendance for student ID {student_id} marked as '{status}' on {cDate} successfully!")

    except Exception as e:
        ui.stop_loading()
        ui.show_error(f"Error marking attendance: {e}")