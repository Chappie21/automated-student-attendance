# Attendance Automation ✅

Automates attendance marking from a classroom list image. Uses the Gemini API (Google GenAI) to extract students who signed and `gspread` to mark presence/absence in a Google Sheets worksheet.

---

## ✨ What this project does

- Analyzes an attendance list image and extracts signed rows (ID, first name, last name) using the prompt in `prompt.txt`.
- Converts the model output into JSON and searches for `id` values in a Google Sheets worksheet.
- Marks "P" (Present) for found IDs and "A" (Absent) for IDs not found in the date column.

---

## 🧰 Requirements

- Python 3.10+ (recommended)
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

## ⚙️ Configuration

1. Create a `.env` file (or set environment variables) with the following values:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_genai_model_name
GOOGLE_CREDS_JSON_PATH=./credentials.json
GOOGLE_SPREADSHEET_KEY=your_spreadsheet_key
```

2. Google Sheets credentials:
   - Create a Service Account in Google Cloud and download the JSON key file (set its path in `GOOGLE_CREDS_JSON_PATH`).
   - Share the spreadsheet with the service account's `client_email` (found in the JSON key file).
   - Get the `GOOGLE_SPREADSHEET_KEY` from the sheet URL (the part after `/d/` and before `/`).

3. Prompt / extraction:
   - Edit `prompt.txt` to adjust extraction rules (expected JSON format, relevant columns, validations, etc.). The model should return a **raw JSON array** (e.g. `[ {"id": 123, ...}, ... ]`).

---

## 🚀 Usage

Main command (requires `--image` and `--seccion`):

```bash
python main.py --image path/to/list.jpg --seccion "YourSectionName" [--date YYYY-MM-DD] [--debugging True]
```

Options:
- `--image, -i`: Path to the list image (required).
- `--seccion, -s`: Worksheet name where attendance will be marked (required).
- `--date, -d`: Date for the column (defaults to today, format `YYYY-MM-DD`).
- `--debugging, -dbg`: Debug mode to print the raw model response.

Internal flow:
1. `GeminiAdapter.generate_from_image()` sends the image and `prompt.txt` content to the model.
2. `convertToList()` extracts the JSON array from the response.
3. `SheetsAdapter` creates/updates the date column and marks `P`/`A` values.

---

## 🔍 Technical notes & limitations

- `prompt.txt` must explicitly request a raw JSON array with the expected structure (`id`, `firstName`, `lastName`).
- `convertToList` extracts the JSON array by finding the first `[` and the last `]`; if no valid array is found it returns `[]`.
- If an ID is not found in the sheet, the script prints a message and the record will not be marked as `P`.
- Common error messages and fixes:
  - `The prompt is empty.` → check `prompt.txt`.
  - `Image not found` → verify the image path.
  - `Spreadsheet '...' not found` → check `GOOGLE_SPREADSHEET_KEY` and service account sharing.
  - Token limits / 429 errors from the model → wait and retry.

---

## 🔐 Security

- **Do not** commit `credentials.json` or `.env` to public repositories.
- Keep API keys and credentials out of version control.

---

## 🛠️ Development & testing

- Use `--debugging True` to inspect the raw model output and debug parsing.
- You can simulate responses by creating test files or temporarily modifying `prompt.txt` for controlled outputs.

---

## 🙋 Contributing

Pull requests are welcome. If you modify `prompt.txt` or the parser behavior, document the change and add manual test notes.

---

If you want, I can also add a `.env.example` and a short `USAGE.md` with examples — should I add those? 💡