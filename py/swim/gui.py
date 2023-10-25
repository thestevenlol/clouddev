# Written by Jack Foley, C00274246

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Select, Label, OptionList, Button, Static
from textual.containers import Container, Horizontal
from textual.screen import Screen
import swimming_utils as swimdata
import webbrowser

raw = swimdata.get_all_files()
names = swimdata.get_names()
data = []
text = ""
option_list = OptionList()
select = Select((line, line) for line in names)
return_button = Button("Yes", id="return_button", variant="success")
exit_button = Button("No", id="exit_button", variant="error")
button_container = Container(
    Static("Do you want to choose another swimmer?", id="question"),
    Horizontal(
        return_button,
        exit_button,
        classes="buttons"
    ),
    id="container"
)

class ExitScreen(Screen):
    CSS_PATH="exit.tcss"

    def compose(self) -> ComposeResult:
        yield button_container
        

class Swimmers(App):

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    # Initialise all widgets and intall screens
    def compose(self) -> ComposeResult:
        self.title = "Swimming Data"
        self.swimmers_name = None

        yield Header()
        yield Footer()
        yield select

        self.install_screen(ExitScreen(), name="exit")

    # Dark mode toggle
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    # Event handler for exit button on exit screen
    @on(Button.Pressed, selector="#exit_button")
    def on_exit(self):
        self.pop_screen()
        self.exit(0)

    # Event handler for return button on exit screen
    @on(Button.Pressed, selector="#return_button")
    def on_press(self):
        self.pop_screen()

    # Event handler for drop down list on main screen
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:

        # Clear the list, get the name selected and set the name to the title.

        option_list.clear_options()
        self.swimmers_name = event.value
        put = []
        self.title = str(f"{self.swimmers_name}'s Swimming Data")
        
        # If 'Select' is selected, return.

        if event.value is None:
            return

        # Clear the data list and populate

        data.clear()

        for filename in raw:
            if self.swimmers_name in filename:
                data.append(filename)

        # Iterate through data, add to optionlist and avoid adding duplicates.
        for i in data:
            length = i.split('-')[2]
            swim = i.split('-')[3]
            swim = swim.removesuffix(".txt")
            txt = length + " " + swim
            
            if txt in put:
                continue

            option_list.add_option(txt)
            put.append(txt)
        
        # Mount the option list to the GUI.

        self.mount(option_list)

    # Event handler for option list on main screen
    @on(OptionList.OptionSelected)
    def option_selected(self, event: OptionList.OptionSelected):
        index = event.option_index # get index of currently selected index
        option = option_list.get_option_at_index(index).prompt # get prompt from option list using index

        name = self.swimmers_name # get the name from class
        length = option.split()[0] # get the length
        type = option.split()[1] # get the type

        # Iterate through the swimmer's files using get_named_files(name)
        # Check if the swim type and length is in the file name
        # If yes, assign the filename to named
        named = None
        for named_file in swimdata.get_named_files(name):
            if length in named_file and type in named_file:
                named = named_file
                break

        # Get the data from the file using get_data(file)
        data = swimdata.get_data(named)

        # Create the HTML from the data using create_html(data)
        html = swimdata.create_html(data)
        
        # Clear the index.html file by opening it with write permissions and then closing it again.
        open("templates/index.html", "w").close()

        # Open the file and write the HTML data to it.
        with open("templates/index.html", "w") as f:
            f.write(html)

        # Attempt to open in new tab, if none found, open browser and open in new tab.
        webbrowser.open_new_tab("index.html")
            
        # Display the exit screen.
        self.push_screen("exit")



if __name__ == "__main__":
    app = Swimmers()
    app.run()