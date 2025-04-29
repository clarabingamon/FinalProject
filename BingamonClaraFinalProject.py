# budgetappgui_with_radiobuttons.py
from breezypythongui import EasyFrame
from tkinter import PhotoImage, IntVar

class BudgetApp(EasyFrame):
    def __init__(self):
        super().__init__(title="Simple Budgeting App", background="lightgreen")

        # Input for income
        self.addLabel(text="Enter Your Monthly Income:", row=0, column=0, sticky="W", background="lightgreen")
        self.incomeField = self.addFloatField(value=0.0, row=0, column=1)

        # Budget Categories with circle buttons (checkable)
        self.addLabel(text="Select Categories:", row=1, column=0, sticky="W", background="lightgreen")

        self.categoryVars = {
            "Rent": IntVar(),
            "Food": IntVar(),
            "Utilities": IntVar(),
            "Transportation": IntVar(),
            "Entertainment": IntVar(),
            "Savings": IntVar()
        }

        row = 2
        for category, var in self.categoryVars.items():
            self.addCheckbutton(text=category, row=row, column=0, variable=var)
            row += 1

        # Buttons
        self.calculateButton = self.addButton(text="Calculate Budget", row=row, column=0, command=self.calculateBudget)
        self.exitButton = self.addButton(text="Exit", row=row, column=1, command=self.quit)

        # Category percentages
        self.percentages = {
            "Rent": 0.30,
            "Food": 0.15,
            "Utilities": 0.10,
            "Transportation": 0.10,
            "Entertainment": 0.10,
            "Savings": 0.00,  # Savings handled separately
        }

    def calculateBudget(self):
        income = self.incomeField.getNumber()
        selectedCategories = {k: v.get() for k, v in self.categoryVars.items() if v.get() == 1}

        if not selectedCategories:
            self.messageBox(title="Error", message="Please select at least one category!")
            return

        budgetWindow = EasyFrame(title="Budget Breakdown", background="lightgreen")

        # Load icons
        icons = {
            "Rent": PhotoImage(file="rent.png"),
            "Food": PhotoImage(file="food.png"),
            "Utilities": PhotoImage(file="utilities.png"),
            "Transportation": PhotoImage(file="transportation.png"),
            "Entertainment": PhotoImage(file="entertainment.png"),
            "Savings": PhotoImage(file="savings.png"),
        }

        totalAllocated = 0
        row = 0

        for category in selectedCategories:
            amount = income * self.percentages[category]
            totalAllocated += amount
            budgetWindow.addLabel(image=icons[category], row=row, column=0)
            budgetWindow.addLabel(text=f"{category}:", row=row, column=1, sticky="W", background="lightgreen")
            budgetWindow.addLabel(text=f"${amount:.2f}", row=row, column=2, sticky="W", background="lightgreen")
            row += 1

        # Handle leftover for savings
        if "Savings" not in selectedCategories:
            leftover = income - totalAllocated
            budgetWindow.addLabel(image=icons["Savings"], row=row, column=0)
            budgetWindow.addLabel(text="Savings:", row=row, column=1, sticky="W", background="lightgreen")
            budgetWindow.addLabel(text=f"${leftover:.2f}", row=row, column=2, sticky="W", background="lightgreen")

        budgetWindow.addButton(text="Exit", row=row + 1, column=1, columnspan=2, command=budgetWindow.quit)

# Main part of the program
if __name__ == "__main__":
    BudgetApp().mainloop()
