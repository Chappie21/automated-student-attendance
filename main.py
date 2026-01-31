from model.geminiAdapter import GeminiAdapter
from model.sheetsAdapter import SheetsAdapter
from dotenv import load_dotenv
from utils.converter import convertToList
from datetime import datetime
import os
import argparse
import gspread

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", help="Ruta a la imagen", default=None)
    parser.add_argument("--seccion", "-s", help="Course seccion", default="")
    parser.add_argument("--date", "-d", help="Date for attendance (YYYY-MM-DD)", default=None)
    parser.add_argument("--debugging", "-dbg", help="Debug mode flag", default=False)
    args = parser.parse_args()

    if (args.image is None):
        raise ValueError("You must provide an image path using --image or -i")

    if (args.seccion is None) or (args.seccion.strip() == ""):
        raise ValueError("You must provide a course section using --seccion or -s")

    print("************ Attendance Automation Script ************")
    print("-> Starting attendance marking process...")

    client = GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL")
    )

    # read prompt from prompt.txt
    with open("prompt.txt", "r", encoding="utf-8") as f:
        textPrompt = f.read().strip()

    if not textPrompt:
        raise ValueError("The prompt is empty. Please provide a valid prompt in prompt.txt")

    print("-> Analyzing image and extracting text...")

    # Analize list image and get text with assist list
    response = client.generate_from_image(args.image, prompt=textPrompt)

    # parse to array of dicts
    response_dict = convertToList(response)

    if args.debugging:
        print("Response from Gemini API:")
        print(response_dict)
    
    sheet = SheetsAdapter(
        creds_json_path=os.getenv("GOOGLE_CREDS_JSON_PATH"),
        spreadsheet_key=os.getenv("GOOGLE_SPREADSHEET_KEY")
    )

    # Create a new column with the date of today if not exists
    worksheet_name = args.seccion
    worksheet = sheet.get_worksheet(worksheet_name)

    # print(f"-> Updating attendance for section: {worksheet_name} <-")

    # Get all headers
    headers = worksheet.row_values(1)

    # Get today's date or use provided date
    today = args.date if args.date else datetime.now().strftime("%Y-%m-%d")

    # Check if today's date column exists
    if today not in headers:
        col_index = len(headers) + 1
        
        # OPCIÓN A: Insertar columna (Mantiene el formato de la tabla)
        # insert_cols añade una columna vacía y desplaza/extiende el formato
        worksheet.insert_cols([[today]], col=col_index, inherit_from_before=True)

        worksheet.update_cell(1, col_index, today)
        
    else:
        # If it already exists, we look for the column number so we can use it later.
        col_index = headers.index(today) + 1

    # Verify that the ID matches the correct row and mark attendance in the created/existing column.
    for record in response_dict:
        student_id = record.get("id") or record.get("ID") or record.get("Id")

        print(f"Processing student ID: {student_id}")

        if not student_id:
            continue

        try:
            cell = worksheet.find(str(student_id))
            row_number = cell.row

            print(f"Marking attendance for ID {student_id}")

            # Marcar asistencia con "P" (Presente)
            worksheet.update_cell(row_number, col_index, "P")
        except Exception as e:
            print(f"ID {student_id} no encontrado en la hoja '{worksheet_name}'.")

    # Set absences for those not marked present
    all_ids = [str(record.get("id") or record.get("ID") or record.get("Id")) for record in response_dict]
    id_cells = worksheet.col_values(1)[1:]  # exclude header
    for idx, student_id in enumerate(id_cells, start=2):  # start=2 to account for header row
        if student_id not in all_ids:
            print(f"Marking absence for ID {student_id}")
            worksheet.update_cell(idx, col_index, "A")
    
    print("-> Attendance updated successfully. <-")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")