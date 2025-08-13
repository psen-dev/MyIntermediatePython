def register_user():
    print("\n--- Register New Account ---")
    usname = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")

    # Check if passwords match
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    dob = input("Enter date of birth (YYYY-MM-DD): ")
    aadhar = input("Enter Aadhar number: ")
    address = input("Enter address: ")

    # Check if Aadhar number already exists
    cursor.execute("SELECT accno FROM account_details WHERE aadhar = %s", (aadhar,))
    if cursor.fetchone():
        print("Aadhar number already exists. Registration failed.")
        return

    # Insert new user into the database
    try:
        cursor.execute("""
            INSERT INTO account_details (usname, password, dob, aadhar, address, balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (usname, password, dob, aadhar, address, 0.00))
        conn.commit()
        print("Account registered successfully!")
    except Exception as e:
        print("Error during registration:", e)
        
        
def login_user():
    print("\n--- Login to Your Account ---")
    accno = input("Enter your account number: ")
    password = input("Enter your password: ")

    # Check if account number and password match in the database
    cursor.execute("SELECT usname FROM account_details WHERE accno = %s AND password = %s", (accno, password))
    result = cursor.fetchone()

    if result:
        print(f"Welcome back, {result[0]}!")  # Greet the user with their username
        return accno  # Return account number for further actions
    else:
        print("Invalid account number or password. Please try again.")
        return None  # Return None if login fails
    
def transfer_funds(accno):
    print("\n--- Fund Transfer ---")
    target_accno = input("Enter the target account number: ")
    amount = float(input("Enter the amount to transfer: "))

    # Check if the target account exists
    cursor.execute("SELECT accno FROM account_details WHERE accno = %s", (target_accno,))
    target_exists = cursor.fetchone()

    if not target_exists:
        print("Target account does not exist. Transfer failed.")
        return

    # Check balance of the source account
    cursor.execute("SELECT balance FROM account_details WHERE accno = %s", (accno,))
    result = cursor.fetchone()

    if result[0] >= amount:
        # Deduct amount from source account
        cursor.execute("UPDATE account_details SET balance = balance - %s WHERE accno = %s", (amount, accno))

        # Add amount to target account
        cursor.execute("UPDATE account_details SET balance = balance + %s WHERE accno = %s", (amount, target_accno))

        # Commit the transaction
        conn.commit()
        print("Transfer successful!")
    else:
        print("Insufficient balance. Transfer failed.")
        
def apply_for_loan(accno):
    print("\n--- Apply for a Loan ---")
    
    # Loan type input
    loan_type = input("Enter loan type (personal/car/house): ").lower()
    if loan_type not in ['personal', 'car', 'house']:
        print("Invalid loan type. Please choose 'personal', 'car', or 'house'.")
        return
    
    # Set interest rate based on loan type
    if loan_type == 'personal':
        rate = 8.0
    elif loan_type == 'car':
        rate = 10.0
    elif loan_type == 'house':
        rate = 12.0

    # Loan amount input
    amt = float(input("Enter loan amount: "))
    term = int(input("Enter loan term (in months): "))  # Loan duration in months

    # Calculate total repayment amount
    monthly_interest_rate = rate / 12 / 100
    total_repayment_amt = amt * ((1 + monthly_interest_rate) ** term)

    # Default number of installments
    no_installments = 10

    try:
        # Insert loan into the loan table
        cursor.execute("""
            INSERT INTO loan (accno, loan_type, amt, rate, term, total_repayment_amt, no_installments)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (accno, loan_type, amt, rate, term, total_repayment_amt, no_installments))

        # Update the account balance in the account_details table
        cursor.execute("""
            UPDATE account_details
            SET balance = balance + %s
            WHERE accno = %s
        """, (amt, accno))

        # Commit the changes
        conn.commit()
        print("Loan application successful!")
        print(f"Loan Type: {loan_type.capitalize()}, Amount: {amt:.2f}, Interest Rate: {rate:.1f}%, Term: {term} months")
        print(f"Total Repayment Amount: {total_repayment_amt:.2f}, Number of Installments: {no_installments}")
    except Exception as e:
        print("Error applying for loan:", e)
        
import datetime

def loan_repayment(accno):
    try:
        # Take loan ID as input
        loan_id = int(input("Enter the loan ID: "))

        # Get the current date for loan repayment
        loan_repay_date = datetime.date.today()

        # Check if the loan exists and get the current loan details
        cursor.execute("SELECT * FROM loan WHERE loan_id = %s", (loan_id,))
        loan = cursor.fetchone()

        if loan is None:
            print("No such loan found with the given loan ID.")
            return
        
        # Calculate the repayment amount (total repayment amount / 10 installments)
        total_repayment_amt = loan['total_repayment_amt']
        amt_to_be_repaid = total_repayment_amt / 10

        # Check if the account exists
        cursor.execute("SELECT * FROM account_details WHERE accno = %s", (accno,))
        account = cursor.fetchone()

        if account is None:
            print("No such account found with the given account number.")
            return
        
        # Check if the account balance is sufficient for repayment
        current_balance = account['balance']
        if current_balance < amt_to_be_repaid:
            print("Insufficient funds in the account for repayment.")
            return

        # Count how many installments have already been paid for this loan
        cursor.execute("SELECT COUNT(*) FROM loan_repayment WHERE loan_id = %s", (loan_id,))
        installments_paid = cursor.fetchone()[0]

        # Calculate the installment number
        installment_no = installments_paid + 1

        if installment_no > 10:
            print("All installments have been repaid for this loan.")
            return

        # Deduct the repayment amount from the account balance
        new_balance = current_balance - amt_to_be_repaid
        cursor.execute("""
            UPDATE account_details
            SET balance = %s
            WHERE accno = %s
        """, (new_balance, accno))

        # Insert loan repayment record into the loan_repayment table
        cursor.execute("""
            INSERT INTO loan_repayment (loan_id, amt_to_be_repaid, installment_no, loan_repay_date, accno)
            VALUES (%s, %s, %s, %s, %s)
        """, (loan_id, amt_to_be_repaid, installment_no, loan_repay_date, accno))

        # Commit the changes
        conn.commit()

        print(f"Repayment of {amt_to_be_repaid:.2f} for loan ID {loan_id} has been successfully made.")
        print(f"New account balance: {new_balance:.2f}")
        print(f"Installment number: {installment_no}")

    except Exception as e:
        # Handle any errors that occur (without rollback)
        print("Error processing loan repayment:", e)

        

        

