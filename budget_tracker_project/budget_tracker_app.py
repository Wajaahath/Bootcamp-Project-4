# Budget Tracker Application

# Imports
import sqlite3
import os
from datetime import datetime


def create_connection(db_name):
    """
    Creates a connection to the SQLite database and returns the connection
    and cursor.

    :param db_name: The name of the SQLite database.
    :type db_name: str

    :returns: A tuple containing the database connection and cursor.
    :rtype: tuple
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor


def commit_and_close(connection):
    """
    Commits any changes and closes the database connection.

    :param connection: The database connection to commit and close.
    :type connection: sqlite3.Connection
    """
    connection.commit()
    connection.close()


def create_database():
    """
    Initializes the SQLite database and creates necessary tables.

    This function creates the tables for expenses, income, budgets, and
    financial goals. It also pre-populates the tables with example data
    if the database is being created for the first time.
    """
    db_exists = os.path.exists("expense_tracker.db")
    connection, cursor = create_connection("expense_tracker.db")

    # Create tables for expenses and income
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            due_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            pay_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY,
            category TEXT,
            budget_amount REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_goals (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            target_amount REAL,
            saved_amount REAL
        )
    ''')

    # Pre-populate the tables with example data.
    if not db_exists:
        cursor.executemany('''INSERT INTO expenses (category, amount, due_date)
                           VALUES (?, ?, ?)''', [
            ("Groceries", 50.0, "2024-12-01"),
            ("Utilities", 100.0, "2024-12-02"),
            ("Transport", 20.0, "2024-12-03"),
            ("Dining", 30.0, "2024-12-04"),
            ("Entertainment", 40.0, "2024-12-05")
        ])

        cursor.executemany('''INSERT INTO income (category, amount, pay_date)
                           VALUES (?, ?, ?)''', [
            ("Salary", 2000.0, "2024-12-01"),
            ("Freelancing", 500.0, "2024-12-02"),
            ("Investments", 300.0, "2024-12-03"),
            ("Gifts", 100.0, "2024-12-04"),
            ("Other", 50.0, "2024-12-05")
        ])

        cursor.executemany('''INSERT INTO budgets (category, budget_amount)
                           VALUES (?, ?)''', [
            ("Groceries", 300.0),
            ("Utilities", 150.0),
            ("Transport", 100.0),
            ("Dining", 200.0),
            ("Entertainment", 150.0)
        ])

        cursor.executemany('''INSERT INTO financial_goals (goal, target_amount,
                           saved_amount) VALUES (?, ?, ?)''', [
            ("Buy a car", 20000.0, 5000.0),
            ("Vacation", 5000.0, 1500.0),
            ("Emergency fund", 10000.0, 3000.0),
            ("Home renovation", 15000.0, 4000.0),
            ("New laptop", 2000.0, 800.0)
        ])

    commit_and_close(connection)


def get_category(prompt):
    """
    Prompts the user to input a valid expense category.

    The input must be non-empty and cannot contain numbers. It is
    capitalized before being returned.

    :param prompt: The message displayed to the user.
    :type prompt: str

    :returns: A valid, capitalized category name.
    :rtype: str

    :raises ValueError: If the input is empty or contains numbers.

    .. note::
        The function keeps prompting the user until valid input is provided.
    """
    while True:
        try:
            user_input = input(prompt).strip().capitalize()
            if not user_input:  # Check if input is empty.
                raise ValueError("Input cannot be empty!")
            # Check if input contains numbers.
            if any(char.isdigit() for char in user_input):
                raise ValueError("A Category cannot contain numbers!")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid category.")


def get_amount(prompt):
    """
    Prompts the user for a valid float input and ensures input is non-empty.

    :param prompt: The message to display when asking for input.
    :type prompt: str

    :returns: The user's input as a float.
    :rtype: float
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Inout cannot be empty!. Please enter a valid amount.")
            continue
        try:
            return float(user_input)
        except ValueError:
            print("An amount cannot contain characters!."
                  " Please enter a valid amount.")


# Function to get valid date input
def get_date(prompt):
    """
    Prompts the user for a date input in format YYYY-MM-DD and validates it.

    :param prompt: The message to display when asking for input.
    :type prompt: str

    :returns: A valid date object.
    :rtype: datetime.date
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty. Please enter a valid date.")
            continue
        try:
            valid_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            return valid_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def validate_category_input(table_name):
    """
    Validates user input for category by comparing it with existing categories.

    This function fetches distinct categories from the specified table and
    prompts the user to select a valid category from the list.

    :param table_name: The name of the table to fetch categories from.
    :type table_name: str

    :returns: The valid category chosen by the user.
    :rtype: str
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute(f'''SELECT DISTINCT category FROM {table_name}''')
        categories = [row[0] for row in cursor.fetchall()]

        print("Available categories:")
        for category in categories:
            print(f"- {category}")

        while True:
            user_input = input("Enter a category from the list above:"
                               " ").strip().capitalize()
            if user_input in categories:
                connection.close()
                return user_input
            else:
                print("Invalid category. Please choose from the list.")
    except Exception as e:
        print(f"Error: {e}")


def get_financial_goal(prompt):
    """
    Prompts user for a valid financial goal input and ensures it is non-empty.

    :param prompt: The message to display when asking for input.
    :type prompt: str

    :returns: The valid financial goal input.
    :rtype: str
    """
    while True:
        try:
            # Request user input.
            user_input = input(prompt).strip().capitalize()
            if not user_input:  # Check if input is empty.
                raise ValueError("Financial goal cannot be empty!")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid financial goal.")


def validate_financial_goal_input(table_name):
    """
    Validates input for a financial goal by comparing it with existing goals.

    This function fetches distinct financial goals from the specified table and
    prompts the user to select a valid goal from the list.

    :param table_name: The name of the table to fetch goals from.
    :type table_name: str

    :returns: The valid financial goal chosen by the user.
    :rtype: str
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute(f'''SELECT DISTINCT goal FROM {table_name}''')
        goals = [row[0] for row in cursor.fetchall()]

        print("Available categories:")
        for goal in goals:
            print(f"- {goal}")

        while True:
            user_input = input("Enter a financial goal from the list "
                               "above: ").strip().capitalize()
            if user_input in goals:
                connection.close()
                return user_input
            else:
                print("Invalid category. Please choose from the list.")
    except Exception as e:
        print(f"Error: {e}")


# Main logic to insert and add expenses into database.
def add_expense():
    """
    Prompts the user for an expense category, amount, and due date, then
    inserts the expense into the database.
    """
    # Variables for expense
    expense_category = get_category(prompt="Enter an expense category: ")
    expense_amount = get_amount(prompt="Enter an expense amount: ")
    expense_due_date = get_date(prompt="Enter due date (YYYY-MM-DD): ")

    # Insert the expense with the valid inputs into the database.
    insert_expense(expense_category, expense_amount, expense_due_date)


def insert_expense(expense_category, expense_amount, expense_due_date):
    """
    Inserts an expense with a category, amount, and due date into the SQLite
    database if the category does not already exist.

    :param expense_category: The category of the expense.
    :type expense_category: str
    :param expense_amount: The amount of the expense.
    :type expense_amount: float
    :param expense_due_date: The due date of the expense.
    :type expense_due_date: datetime.date

    :raises Exception: If there is an error during the database operation.
    """
    try:
        # Convert the date to ISO format string for SQLite compatibility
        # Convert date to string in the format YYYY-MM-DD
        date_str = expense_due_date.isoformat()
        # Connect to SQLite database
        connection, cursor = create_connection("expense_tracker.db")
        # Insert data into the table ensuring that it does not already exists.
        cursor.execute('''SELECT category FROM expenses
                       WHERE category = ?''', (expense_category,))
        if cursor.fetchone():
            print("Category already exists. Please update the existing"
                  " category or use a different name.")
        else:
            cursor.execute('''INSERT INTO expenses (category, amount, due_date)
                           VALUES (?, ?, ?)''',
                           (expense_category, expense_amount, date_str))
            print("Expense added successfully!")
        commit_and_close(connection)
    except Exception as e:
        print(f"Error: {e}")


def view_expenses():
    """
    Retrieves and displays all expenses stored in the SQLite database.

    This function fetches and prints all expenses in the database, including
    their ID, category, amount, and due date.

    :raises Exception: If there is an error during database operations.

    :variables:
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT * FROM expenses''')
        rows = cursor.fetchall()

        print("\nExpenses:")
        for row in rows:
            print(f"ID: {row[0]}, Category: {row[1]}, Amount: {row[2]},"
                  f" Due date: {row[3]}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def view_expenses_by_category():
    """
    Retrieves and displays expense records filtered by a specified category.

    This function prompts the user to select a category from the available
    expense categories, and then fetches and displays all expense entries in
    that category. The details displayed include the ID, amount, and due date
    for each expense record.

    :raises Exception: If there is an error connecting to the database,
                        validating the category, or retrieving the filtered
                        income data.

    :variables:
        - `income_category` (str): The category of income to retrieve.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        expense_category = validate_category_input("expenses")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT * FROM expenses WHERE category = ?''',
                       (expense_category,))
        rows = cursor.fetchall()

        print(f"\nExpenses in category '{expense_category}':")
        for row in rows:
            print(f"ID: {row[0]}, Amount: {row[2]}, Due date: {row[3]}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def update_expense():
    """
    Updates the expense amount for a specified category in the database.

    This function prompts the user to select a category and enter a new
    expense amount. The specified category's expense is updated in the
    database with the new amount.

    :raises Exception: If there is an error during the database operation.

    :variables:
        - `expense_category` (str): The category of the expense to update.
        - `new_amount` (float): The new expense amount.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        print("\n--- Update An Expense Amount ---")
        expense_category = validate_category_input("expenses")
        new_amount = get_amount(prompt="Enter a new expense amount: ")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''UPDATE expenses SET amount = ? WHERE category = ?''',
                       (new_amount, expense_category))
        commit_and_close(connection)
        print(f"Expense updated successfully for"
              f" category '{expense_category}'.")
    except Exception as e:
        print(f"Error: {e}")


def delete_expense():
    """
    Deletes an expense and corresponding budget by category from the database.

    The function prompts the user for a category, then deletes the expense
    from the expenses table and the corresponding budget from budgets table.

    :raises Exception: If there is an error during the database operation.
    """
    try:
        print("\n--- Delete An Expense ---")
        category = validate_category_input("expenses")
        connection, cursor = create_connection("expense_tracker.db")
        # Delete the expense from the expenses table
        cursor.execute("DELETE FROM expenses WHERE category = ?", (category,))
        # Delete the corresponding budget from the budgets table
        cursor.execute("DELETE FROM budgets WHERE category = ?", (category,))
        commit_and_close(connection)
        print(f"Expense and corresponding budget deleted successfully for"
              f" category '{category}'.")
    except Exception as e:
        print(f"Error: {e}")


def total_expenses():
    """
    Calculates and displays the total amount of all expenses.

    This function retrieves the sum of all expense amounts from the database
    and displays the total.

    :raises Exception: If there is an error during the database operation.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT SUM(amount) FROM expenses''')
        total = cursor.fetchone()[0]

        if total is None:
            total = 0.0
        print(f"Total Expenses: {total}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def add_income():
    """
    Prompts the user for an income category, amount, and pay date, then
    inserts the income into the database.
    """
    income_category = get_category(prompt="Enter an income category: ")
    income_amount = get_amount(prompt="Enter an income amount: ")
    income_pay_date = get_date(prompt="Enter pay date (YYYY-MM-DD): ")

    # Insert the income with the valid inputs into the database.
    insert_income(income_category, income_amount, income_pay_date)


def insert_income(income_category, income_amount, income_pay_date):
    """
    Inserts an income with a category, amount, and pay date into the SQLite
    database if the category does not already exist.

    :param income_category: The category of the income.
    :type income_category: str
    :param income_amount: The amount of the income.
    :type income_amount: float
    :param income_pay_date: The pay date of the income.
    :type income_pay_date: datetime.date

    :raises Exception: If there is an error during the database operation.
    """
    # Convert the date to ISO format string for SQLite compatibility
    # Convert date to string in the format YYYY-MM-DD
    try:
        date_str = income_pay_date.isoformat()
        # Connect to SQLite database
        connection, cursor = create_connection("expense_tracker.db")
        # Insert data into the table ensuring that it does bot already exists.
        cursor.execute('''SELECT category FROM income WHERE category = ?''',
                       (income_category,))
        if cursor.fetchone():
            print("Category already exists. Please update the existing"
                  " category or use a different name.")
        else:
            cursor.execute('''INSERT INTO income (category, amount, pay_date)
                           VALUES (?, ?, ?)''',
                           (income_category, income_amount, date_str))
            print("Income added successfully!")
        commit_and_close(connection)
    except Exception as e:
        print(f"Error: {e}")


def view_income():
    """
    Retrieves and displays all incomes stored in the SQLite database.

    This function fetches and prints all income in the database, including
    their ID, category, amount, and pay date.

    :raises Exception: If there is an error during database operations.

    :variables:
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT * FROM income''')
        rows = cursor.fetchall()

        print("\nIncome:")
        for row in rows:
            print(f"ID: {row[0]}, Category: {row[1]}, Amount: {row[2]},"
                  f" Pay date: {row[3]}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def view_income_by_category():
    """
    Retrieves and displays income records filtered by a specified category.

    This function prompts the user to select a category from the available
    income categories, and then fetches and displays all income entries in that
    category. The details displayed include the ID, amount, and pay date for
    each income record.

    :raises Exception: If there is an error connecting to the database,
                        validating the category, or retrieving the filtered
                        income data.

    :variables:
        - `income_category` (str): The category of income to retrieve.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        income_category = validate_category_input("income")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT * FROM income WHERE category = ?''',
                       (income_category,))
        rows = cursor.fetchall()

        print(f"\nIncome in category '{income_category}':")
        for row in rows:
            print(f"ID: {row[0]}, Amount: {row[2]}, Pay date: {row[3]}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def update_income():
    """
    Updates the income amount for a specified category.

    This function prompts the user to select an income category and enter a
    new income amount. The income record for the selected category is then
    updated with the new amount in the SQLite database.

    :raises Exception: If there is an error connecting to database, updating
                        the income record, or validating the category input.

    :variables:
        - `income_category` (str): The category of the income to update.
        - `new_amount` (float): The new income amount.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        print("\n--- Update An Income Amount ---")
        income_category = validate_category_input("income")
        new_amount = get_amount(prompt="Enter a new income amount: ")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''UPDATE income SET amount = ? WHERE category = ?''',
                       (new_amount, income_category))
        commit_and_close(connection)
        print(f"Income updated successfully for category '{income_category}'.")
    except Exception as e:
        print(f"Error: {e}")


def delete_income():
    """
    Deletes an income record by category.

    This function prompts the user to select an income category and then
    removes the corresponding income record from the SQLite database.

    :raises Exception: If there is an error connecting to database, deleting
                        the income record, or validating the category input.
    """
    try:
        print("\n--- Delete An Income ---")
        income_category = validate_category_input("income")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''DELETE FROM income WHERE category = ?''',
                       (income_category,))
        commit_and_close(connection)
        print(f"Income deleted successfully for category '{income_category}'.")
    except Exception as e:
        print(f"Error: {e}")


def total_income():
    """
    Calculates and displays the total income from the database.

    This function queries the database to sum all income amounts and displays
    the total. If no income records exist, it will display a total of 0.0.

    :raises Exception: If there is an error connecting to the database or
                        fetching the income data.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT SUM(amount) FROM income''')
        total = cursor.fetchone()[0]

        if total is None:
            total = 0.0
        print(f"Total Income: {total}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def set_budget():
    """
    Sets or updates the budget for a specific category.

    This function prompts the user to choose a category and then sets or
    updates the budget amount for that category in the database. If a budget
    already exists for the category, it is replaced with the new budget amount.

    :raises Exception: If there is an error connecting to the database or
                        updating the budget.
    """
    try:
        print("\n--- Set A Budget Amount ---")
        budget_category = validate_category_input("expenses")
        budget_amount = get_amount(prompt="Enter budget amount: ")
        connection, cursor = create_connection("expense_tracker.db")
        # Check if the category already exists
        cursor.execute('''SELECT budget_amount
                       FROM budgets
                       WHERE category = ?''', (budget_category,))
        existing_budget = cursor.fetchone()

        if existing_budget:
            # Update the existing budget
            cursor.execute('''
                UPDATE budgets
                SET budget_amount = ?
                WHERE category = ?
            ''', (budget_amount, budget_category))
            print(f"Budget for category '{budget_category}' "
                  f"updated successfully!")
        else:
            # Insert a new budget
            cursor.execute('''
                INSERT INTO budgets (category, budget_amount)
                VALUES (?, ?)
            ''', (budget_category, budget_amount))
            print(f"Budget for category '{budget_category}' set successfully!")
        commit_and_close(connection)
    except Exception as e:
        print(f"Error: {e}")


def view_budget():
    """
    Displays the budget for a specific category.

    This function prompts the user to choose a category and then retrieves
    and displays the associated budget from the database. If no budget exists
    for the specified category, it informs the user that no budget is found.

    :raises Exception: If there is an error connecting to the database or
                        retrieving the budget.

    :variables:
    :variables:
        - `budget_category` (str): The category of budgets to retrieve.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        budget_category = validate_category_input("expenses")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT budget_amount FROM budgets
                       WHERE category = ?''', (budget_category,))
        result = cursor.fetchone()

        if result:
            print(f"Budget for {budget_category}: {result[0]}")
        else:
            print("No budget found for this category.")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def set_financial_goal():
    """
    Set a financial goal, including the target and saved amounts.

    This function prompts the user to enter a financial goal, a target amount,
    and the amount saved so far. The information is then saved into database.

    :raises Exception: If there is an error connecting to the database or
                        inserting the financial goal.
    """
    try:
        financial_goal = get_financial_goal(prompt="Enter a financial goal: ")
        target_amount = get_amount(prompt="Enter target amount: ")
        saved_amount = get_amount(prompt="Enter saved amount: ")
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''INSERT INTO financial_goals
                       (goal, target_amount, saved_amount) VALUES (?, ?, ?)''',
                       (financial_goal, target_amount, saved_amount))
        commit_and_close(connection)
        print("Financial goal set successfully!")
    except Exception as e:
        print(f"Error: {e}")


def update_financial_goal():
    """
    Update the saved amount for a specific financial goal.

    This function allows the user to update the amount saved for a given
    financial goal. It first fetches the current saved amount, prompts the
    user for the new amount, and updates the database.

    :raises Exception: If there is an error with the database connection,
                        fetching the current saved amount, or updating the
                        saved amount.

    :variables:
        - `financial_goal` (str): The financial_goal of the financial_goals to
            update.
        - `new_saved_amount` (float): The new financial goal saved amount.
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        print("\n--- Update Financial Goal Saved Amount ---")
        financial_goal = validate_financial_goal_input("financial_goals")
        # Fetch the current saved amount
        cursor.execute('''SELECT * FROM financial_goals WHERE goal = ?''',
                       (financial_goal,))
        result = cursor.fetchone()
        current_saved_amount = result[3]

        print(f"Current saved amount for "
              f"'{financial_goal}': {current_saved_amount}")
        new_saved_amount = get_amount(prompt="Enter a new saved amount: ")
        cursor.execute('''UPDATE financial_goals SET saved_amount = ?
                       WHERE goal = ?''', (new_saved_amount, financial_goal))
        commit_and_close(connection)
        print(f"Saved amount for financial goal '{financial_goal}' "
              f"updated successfully!")
    except Exception as e:
        print(f"Error: {e}")


def delete_financial_goal():
    """
    Delete a financial goal by its goal name.

    This function prompts the user to select a financial goal to delete.
    It then removes the corresponding goal from the database.

    :raises Exception: If there is an error with the database connection or
                        deletion of the financial goal.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        print("\n--- Delete Financial Goal ---")
        financial_goal = validate_financial_goal_input("financial_goals")
        # Delete the financial goal
        cursor.execute('''DELETE FROM financial_goals WHERE goal = ?''',
                       (financial_goal,))
        commit_and_close(connection)
        print(f"Financial goal '{financial_goal}' deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")


def view_financial_goals():
    """
    View progress towards financial goals.

    This function retrieves all financial goals from the database and displays
    each goal's name, target amount, and saved amount, allowing the user to
    track their progress.

    :raises Exception: If there is an error with the database connection or
                        fetching the financial goals.

    :variables:
        - `connection` (sqlite3.Connection): The database connection object.
        - `cursor` (sqlite3.Cursor): The database cursor object.
    """
    try:
        connection, cursor = create_connection("expense_tracker.db")
        cursor.execute('''SELECT * FROM financial_goals''')
        rows = cursor.fetchall()

        print("\nFinancial Goals:")
        for row in rows:
            print(f"ID: {row[0]}, Goal: {row[1]}, Target Amount: {row[2]},"
                  f" Saved Amount: {row[3]}")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def budget_summary():
    """
    Provide a detailed summary of current budget, including income, expenses,
    and budget analysis. This function retrieves and calculates total income,
    total expenses, and the total budgeted amounts. It then compares the actual
    expenses for each category to the set budget and provides a status report
    of whether each category is over budget or has no budget set. Additionally,
    it tracks the progress towards financial goals, indicating whether
    any goals have been achieved.

    The summary includes the following:
    - Total income for the user
    - Total expenses for the user
    - Total budgeted amount across all categories
    - Comparison of actual spending versus budgeted amounts by category
    - The remaining balance (income minus expenses)
    - The overall budget status (within budget or over budget)
    - A breakdown of over-budget categories, if applicable
    - A list of categories that do not have a budget set
    - The status of financial goals (achieved or in progress)

    :raises Exception: This function raises an exception if there are any
                        errors related to the database connection,
                        query execution, or data fetching. Examples of such
                        errors include issues with connecting to the database
                        or malformed queries.

    :note: This function assumes that the income, expenses, budgets, and
            financial goals tables exist in the database.
    """
    connection, cursor = create_connection("expense_tracker.db")
    # Total income
    cursor.execute('''SELECT SUM(amount) FROM income''')
    total_income = cursor.fetchone()[0] or 0.0

    # Total expenses
    cursor.execute('''SELECT SUM(amount) FROM expenses''')
    total_expenses = cursor.fetchone()[0] or 0.0

    # Total budgeted amount
    cursor.execute('''SELECT SUM(budget_amount) FROM budgets''')
    total_budgeted = cursor.fetchone()[0] or 0.0

    # Compare each category's expenses and budgets
    cursor.execute('''SELECT category, SUM(amount)
                   FROM expenses GROUP BY category''')
    expense_categories = cursor.fetchall()

    over_budget_categories = []
    no_budget_categories = []
    for category, expense_amount in expense_categories:
        cursor.execute('''SELECT budget_amount
                       FROM budgets
                       WHERE category = ?''', (category,))
        budget_amount = cursor.fetchone()
        if budget_amount is None:
            no_budget_categories.append((category, expense_amount))
        elif expense_amount > budget_amount[0]:
            over_budget_categories.append((category, expense_amount,
                                           budget_amount[0]))

    # Calculate remaining balance
    balance = (total_income - total_expenses)

    # Determine budget status
    if total_expenses <= total_budgeted and balance > 0:
        budget_status = "within budget"
    else:
        budget_status = "over budget"

    # Display the summary
    print("\n----- Budget Summary -----")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Total Budgeted Amount: {total_budgeted}")
    print(f"Remaining Balance (Income - Expenses): {balance}")
    print(f"Overall Spending Status: {budget_status}")

    if over_budget_categories:
        print("\nOver Budget Categories:")
        for category, expense, budget in over_budget_categories:
            print(f" - {category}: Spent {expense}, Budgeted {budget}")
    else:
        print("\nNo categories are over budget.")

    if no_budget_categories:
        print("\nCategories with No Budget Set:")
        for category, expense in no_budget_categories:
            print(f" - {category}: Spent {expense}, Budgeted None")
    else:
        print("\nAll expense categories have budgets set.")
    # Financial goals achieved
    cursor.execute('''SELECT goal FROM financial_goals
                   WHERE saved_amount >= target_amount''')
    achieved_goals = cursor.fetchall()

    print("\n--- Financial Goals Status ---")
    if achieved_goals:
        print("Financial goals achieved:")
        for (goal,) in achieved_goals:
            print(f"- {goal}")
    else:
        print("In Progress")
    connection.close()


def expense_menu():
    """
    Displays the expense-related submenu, allowing the user to perform
    various operations related to expenses. It provides a menu of options
    for the user to choose from, and executes corresponding functions
    based on the user's input.

    **Flow**:
        The function enters an infinite loop, presenting the expense submenu
        until the user selects the option to return to the main menu.
        Based on the user's choice, the corresponding function is executed.
        If the user enters an invalid option, they are prompted to try again.

    **Returns**:
        None: The function does not return any values. It performs actions
        based on user input, such as adding, viewing, updating, or deleting
        expenses.

    **Exceptions**:
        - No explicit exceptions are raised in this function, but the functions
          called within this menu (e.g., `add_expense()`, `view_expenses()`)
          may raise exceptions that should be handled in those respective
          functions.
    """
    while True:
        print("\nExpense Menu")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View expenses by category")
        print("4. Update expense")
        print("5. Delete expense")
        print("6. Total expenses")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_expenses_by_category()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            total_expenses()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def income_menu():
    """
    Displays the income-related submenu, allowing the user to perform various
    operations related to income. It presents a menu of options and executes
    the corresponding function based on the user's input.

    **Flow**:
        The function enters an infinite loop, displaying the income submenu
        until the user selects the option to return to the main menu. Based
        on the user's choice, the corresponding function is executed. If the
        user enters an invalid option, they are prompted to try again.

    **Returns**:
        None: The function does not return any values. It performs actions
        based on user input, such as adding, viewing, updating, or deleting
        income.

    **Exceptions**:
        - No explicit exceptions are raised in this function, but the functions
          called within this menu (e.g., `add_income()`, `view_income()`)
          may raise exceptions that should be handled in those respective
          functions.
    """
    while True:
        print("\nIncome Menu")
        print("1. Add income")
        print("2. View income")
        print("3. View income by category")
        print("4. Update income")
        print("5. Delete income")
        print("6. Total income")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_income()
        elif choice == "2":
            view_income()
        elif choice == "3":
            view_income_by_category()
        elif choice == "4":
            update_income()
        elif choice == "5":
            delete_income()
        elif choice == "6":
            total_income()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def budget_menu():
    """
    Displays the budget-related submenu, allowing the user to set or view
    the budget for a specific category. It provides options to set a new
    budget or view an existing budget for a particular category.

    **Flow**:
        The function enters an infinite loop, displaying the budget submenu
        until the user selects the option to return to the main menu. Based
        on the user's input, the corresponding function is executed. If the
        user enters an invalid option, they are prompted to try again.

    **Returns**:
        None: The function does not return any values. It performs actions
        based on the user's choice, such as setting or viewing a budget.

    **Exceptions**:
        - No explicit exceptions are raised in this function, but the functions
          called within this menu (e.g., `set_budget()`, `view_budget()`)
          may raise exceptions that should be handled in those respective
          functions.
    """
    while True:
        print("\nBudget Menu")
        print("1. Set budget for a category")
        print("2. View budget for a category")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            set_budget()
        elif choice == "2":
            view_budget()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def financial_goals_menu():
    """
    Displays the financial goals-related submenu, allowing the user to set,
    view, update, or delete financial goals. It provides options to manage
    financial goals and track progress towards achieving them.

    **Flow**:
        The function enters an infinite loop, displaying the financial goals
        submenu until the user selects the option to return to the main menu.
        Based on the user's input, the corresponding function is executed.
        If the user enters an invalid option, they are prompted to try again.

    **Returns**:
        None: The function does not return any values. It performs actions
        based on the user's choice, such as setting, viewing, updating, or
        deleting financial goals.

    **Exceptions**:
        - No explicit exceptions are raised in this function, but the functions
          called within this menu (e.g., `set_financial_goal()`,
          `view_financial_goals()`) may raise exceptions that should be handled
          in those respective functions.
    """
    while True:
        print("\nFinancial Goals Menu")
        print("1. Set financial goals")
        print("2. View progress towards financial goals")
        print("3. Update a financial goal")
        print("4. Delete a financial goal")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            set_financial_goal()
        elif choice == "2":
            view_financial_goals()
        elif choice == "3":
            update_financial_goal()
        elif choice == "4":
            delete_financial_goal()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def main_menu():
    """
    Displays the main menu of the Expense and Budget Tracker application and
    handles user choices by directing them to different submenus or actions
    related to managing expenses, income, budgets, financial goals, and
    summaries.

    The available menu options are:
    1. Expense Options (Leads to the expense-related submenu)
    2. Income Options (Leads to the income-related submenu)
    3. Budget Options (Leads to the budget-related submenu)
    4. Financial Goals Options (Leads to the financial goals-related submenu)
    5. Budget Summary (Displays an overview of budget-related information)
    6. Quit (Exits the program)

    **Flow**:
        The function first initializes the database using `create_database()`.
        Then, it enters an infinite loop that displays the main menu options.
        The user is prompted to choose an option by entering the corresponding
        number. Based on the user's choice, the appropriate function is called
        to manage expenses, income, budgets, financial goals, or view a
        summary. If the user chooses to quit, the program exits.

    **Returns**:
        None: The function does not return any values. It manages user
        navigation through the menu system and triggers the appropriate actions
        based on user input.

    **Exceptions**:
        - No explicit exceptions are raised in this function, but the functions
          called within the menu (e.g., `expense_menu()`,
          `income_menu()`, etc.) may raise exceptions that should be handled in
          those respective functions.
    """
    create_database()

    while True:
        print("\nExpense and Budget Tracker")
        print("1. Expense Options")
        print("2. Income Options")
        print("3. Budget Options")
        print("4. Financial Goals Options")
        print("5. Budget Summary")
        print("6. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            expense_menu()
        elif choice == "2":
            income_menu()
        elif choice == "3":
            budget_menu()
        elif choice == "4":
            financial_goals_menu()
        elif choice == "5":
            budget_summary()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
