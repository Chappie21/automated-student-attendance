import os
import questionary
from rich.console import Console
from rich.panel import Panel

class AttendanceUI:
    def __init__(self):
        self.console = Console()
        self.version = os.getenv("TOOL_VERSION", "v1.0.0")
        self.author = "[bold green][link=https://github.com/Chappie21]Chappie21[/link][/bold green]"
        self._active_status = None

    def clean_console(self):
        # clear console
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        # Display the header panel
        self.console.print(Panel(
            f"[bold cyan]Interactive console tool to automate student support attendance marking.[/bold cyan]\n"
            f"[bold yellow]Select an option from the menu below to proceed.[/bold yellow]\n\n"
            f"-> developed by {self.author}",
            title="Attendance Automation Script",
            subtitle=self.version,
            expand=False,
            border_style="cyan"
        ))

    def main_menu(self):
        # Display the main menu and return the user's choice
        choice = questionary.select(
            "Please choose an option:",
            choices=[
                "1. Search for photo and evaluate attendance",
                "2. Mark attendance in Google Sheets",
                "3. Help",
                "4. Exit"
            ],
            style=questionary.Style([
                ('pointer', 'fg:#00ff00 bold'),
                ('highlighted', 'fg:#00ffff bold'),
                ('answer', 'fg:#ffffff bold'),
            ])
        ).ask()
        
        # Extract the numeric choice
        return int(choice.split(".")[0])
    
    def help_menu(self):
        # Display help information
        help_text = (
            "This tool helps automate the process of marking student attendance.\n\n"
            "1. Search for photo and evaluate attendance: Upload a photo and let the system analyze it to mark attendance.\n"
            "2. Mark attendance in Google Sheets: Connect to your Google Sheets and update attendance records.\n\n"
            
            "[bold yellow]To see how to set up Google Sheets integration, please refer to the README.md file.[/bold yellow]\n\n"
            f"If you have any questions or issue, feel free to contact me in github: {self.author}"
        )
        self.console.print(Panel(help_text, title="Help", border_style="blue"))

    def request_input(self, question, placeholder=""):
        # Request input from the user
        self.console.print(f"\n[bold cyan]?[/bold cyan] {question}")
        response = questionary.text(placeholder).ask()
        return response.strip('"').strip("'") if response else None

    def start_loading(self, message):
        # Start a loading spinner with a message
        self._active_status = self.console.status(f"[bold green]{message}...[/bold green]", spinner="dots")
        self._active_status.start()

    def update_loading(self, message):
        # Update the loading spinner message
        if self._active_status:
            self._active_status.update(f"[bold green]{message}...[/bold green]")

    def stop_loading(self, success_msg=None):
        # Stop the loading spinner
        if self._active_status:
            self._active_status.stop()
            self._active_status = None
        if success_msg:
            self.show_success(success_msg)

    def show_error(self, message):
        # Display an error message
        self.console.print(f"\n[bold red]❌ Error:[/bold red] {message}")

    def show_success(self, message):
        # Display a success message
        self.console.print(f"\n[bold green]✅ Success:[/bold green] {message}")

    def show_info(self, message):
        # Display an informational message
        self.console.print(f"\n[bold blue]ℹ️ Info:[/bold blue] {message}")