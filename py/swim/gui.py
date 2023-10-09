from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Select, Label, OptionList
import main as swimdata

raw = swimdata.get_all_files()
names = swimdata.get_names()
data = []
text = ""
option_list = OptionList()

class Swimmers(App):

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        self.title = "Swimming Data"

        yield Header()
        yield Footer()
        yield Select((line, line) for line in names)
        yield Label(text)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:

        # Clear the list, get the name selected and set the name to the title.

        option_list.clear_options()
        name = event.value
        self.title = str(f"{name}'s Swimming Data")
        
        # If 'Select' is selected, return.

        if event.value is None:
            return

        # Cleartthe data list and populate

        data.clear()

        for filename in raw:
            if name in filename:
                data.append(filename)

        # Iterate through data, add to optionlist and avoid adding duplicates.

        put = []
        for i in data:
            length = data[0].split('-')[2]
            
            if length in put:
                continue

            option_list.add_option(length)
            put.append(length)
        
        # Mount the option list to the GUI.

        self.mount(option_list)

if __name__ == "__main__":
    app = Swimmers()
    app.run()