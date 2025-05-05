from breezypythongui import EasyFrame
from tkinter import PhotoImage, Label, Tk, IntVar

class BudgetApp(EasyFrame):
    def __init__(self):
        """
        Initialize the main frame, set up labels, buttons, check buttons, 
        and define category percentages for budget allocation.
        """
        super().__init__(title="Smart Saver", background="lightgreen")

        # Label and input field for monthly income
        self.addLabel(text="Enter Your Monthly Income:", row=0, column=0, sticky="W", background="lightgreen")
        self.incomeField = self.addFloatField(value=0.0, row=0, column=1)

        # Label for category selection
        self.addLabel(text="Select Categories:", row=1, column=0, sticky="W", background="lightgreen")

        # Dictionary to store categories
        self.categoryVars = {
            "Rent": IntVar(),
            "Food": IntVar(),
            "Utilities": IntVar(),
            "Transportation": IntVar(),
            "Entertainment": IntVar(),
     }

        # Create check buttons for each category and position them on the window
        row = 2
        for category in self.categoryVars:
            self.addCheckbutton(text=category, row=row, column=0, 
                                command=lambda cat=category: self.onCheckbuttonChange(cat))
            row += 1

        # Button to calculate the budget breakdown
        self.calculateButton = self.addButton(text="Calculate Budget", row=row, column=0, command=self.calculateBudget)
        # Exit button to close the application
        self.exitButton = self.addButton(text="Exit", row=row, column=1, command=self.quit)

        # Define default percentages for each category
        self.percentages = {
            "Rent": 0.30,
            "Food": 0.15,
            "Utilities": 0.10,
            "Transportation": 0.10,
            "Entertainment": 0.10,
            "Savings": 0.00,  # Savings will be handled separately
        }

        # Load icons for each category (Make sure the images exist in the same folder as the Python file)
        try:
            self.icons = {
                "Rent": PhotoImage(file="rent.png"),
                "Food": PhotoImage(file="food.png"),
                "Utilities": PhotoImage(file="utilities.png"),
                "Transportation": PhotoImage(file="transportation.png"),
                "Entertainment": PhotoImage(file="entertainment.png"),
                "Savings": PhotoImage(file="savings.png"),
            }
            print("Icons loaded successfully")
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.icons = {}  # In case images fail to load, prevent crashes

    def onCheckbuttonChange(self, category):
        """
        Update the category variable when a checkbutton is toggled.
        This is called when any checkbutton is clicked.
        """
        # Toggle the corresponding category's selected value
        var = self.categoryVars[category]
        var.set(1 if var.get() == 0 else 0)

    def calculateBudget(self):
        """
        This function is called when the 'Calculate Budget' button is clicked.
        It calculates the budget allocation for each selected category and displays it.
        """
        income = self.incomeField.getNumber()

        # If the income is empty or zero, show an error message
        if income <= 0:
            self.messageBox(title="Error", message="Please enter a valid income!")
            return

        # Get selected categories by checking which categories are selected (1 = selected)
        selectedCategories = {k: v.get() for k, v in self.categoryVars.items() if v.get() == 1}

        # If no category is selected, show an error message
        if not selectedCategories:
            self.messageBox(title="Error", message="Please select at least one category!")
            return

        # Create a new window to show the budget breakdown
        budgetWindow = EasyFrame(title="Budget Breakdown", background="lightgreen")

        totalAllocated = 0  # To track the total allocated budget
        row = 0  # Starting row for labels in the budget breakdown window

        # Loop through each selected category, calculate and display the budget allocation
        for category in selectedCategories:
            amount = income * self.percentages[category]
            totalAllocated += amount

            # Display the category with an icon and budget amount
            # Here we are using the tkinter Label widget to display images
            icon_label = Label(budgetWindow, image=self.icons[category])
            icon_label.grid(row=row, column=0)

            # Add a label for the category name
            budgetWindow.addLabel(text=f"{category}:", row=row, column=1, sticky="W", background="lightgreen")
            # Add a label for the budget amount
            budgetWindow.addLabel(text=f"${amount:.2f}", row=row, column=2, sticky="W", background="lightgreen")
            row += 1

        # Handle any leftover amount (for savings)
        if "Savings" not in selectedCategories:
            leftover = income - totalAllocated
            icon_label = Label(budgetWindow, image=self.icons["Savings"])
            icon_label.grid(row=row, column=0)

            # Display savings
            budgetWindow.addLabel(text="Savings:", row=row, column=1, sticky="W", background="lightgreen")
            budgetWindow.addLabel(text=f"${leftover:.2f}", row=row, column=2, sticky="W", background="lightgreen")

        # Add an Exit button to the budget breakdown window
        budgetWindow.addButton(text="Exit", row=row + 1, column=1, columnspan=2, command=budgetWindow.quit)

# Main program to launch the GUI
if __name__ == "__main__":
    BudgetApp().mainloop()
