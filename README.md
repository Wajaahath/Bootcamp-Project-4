📝 EXPENSE AND BUDGET TRACKER

Expense and Budget Tracker is a Python-based application designed to simplify personal financial management. It provides a command-line interface (CLI) for tracking expenses, income, budgets, and financial goals, all backed by an SQLite database for secure and persistent storage.

This program is ideal for users who want to gain better control over their finances by categorizing expenses, setting budgets, monitoring income, and achieving financial goals with real-time insights.

🚀 Features
- Expense Tracking
  - Add expenses with categories (e.g., Groceries, Utilities).
  - View all recorded expenses or filter them by category.
  - Update existing expense records.
  - Delete specific expenses when no longer needed.

- Income Management
  - Log various income sources (e.g., Salary, Freelancing).
  - View all income records or filter by specific categories.
  - Update and delete income entries as needed.
  - Calculate total income to assess financial stability.

- Budgeting
  - Set budgets for different categories to control spending.
  - View budgets for specific categories or across all categories.
  - Compare actual expenses against budgeted amounts for better planning.

- Financial Goals
  - Define financial goals with a target amount and track progress.
  - Update saved amounts as you make progress toward your goals.
  - View all goals to stay motivated and delete goals when achieved.

- Summaries and Insights
  - Calculate and display total expenses, income, and remaining balance.
  - View a detailed budget summary with over-budget and under-budget categories.
  - Check progress toward financial goals to celebrate achievements.

🖥️ How It Works

Data Management
- The program uses SQLite, a lightweight, file-based database, to store all financial data. Tables are created for expenses, income, budgets, and financial goals during the initial setup.
- All data persists across sessions, allowing users to resume where they left off.

User Interaction
- The CLI guides users through a menu-driven interface.
- Users select actions like adding expenses, setting budgets, or viewing summaries from the main menu.
- All inputs are validated to ensure data accuracy (e.g., correct date formats, valid numerical values).

🔧 Menu Structure
- Add Expense/Income: Prompts for category, amount, and date, then saves the data.
- View Records: Displays all or filtered data from the database.
- Set Budget: Allows users to assign budget amounts to specific categories.
- Manage Financial Goals: Facilitates goal setting, updating progress, and tracking achievements.
- Summaries: Calculates totals for income and expenses, checks budget adherence, and lists goals achieved.
- Update/Delete: Modify or remove records from any category.
- Exit: Safely exits the program, preserving all data.

🖋️ Example Workflow
- Start the program and set a budget for the "Groceries" category.
- Add an expense for $50 under "Groceries" with a due date.
- View all expenses to confirm the entry.
- Add income from a salary source and track total earnings.
- Create a financial goal (e.g., Save $10,000 for a vacation).
- Periodically update the saved amount for the vacation goal.
- View the budget summary to check spending against the budget.
- Achieve financial goals and celebrate progress!

🛠️ Requirements
- Python 3.6 or higher
- SQLite (included with Python)
