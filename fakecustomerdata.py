from faker import Faker
import random
import pandas as pd

# Create a Faker instance
fake = Faker()

# Generate synthetic customer details
def generate_customer_data(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'CustomerID': fake.unique.random_number(digits=6),
            'Name': fake.name(),
            'Age': random.randint(18, 65),
            'Gender': random.choice(['Male', 'Female']),
            'Email': fake.email(),
            'Address': fake.address()
        }
        customers.append(customer)
    return customers

# Generate synthetic transaction data
def generate_transaction_data(num_transactions, customer_data):
    transactions = []
    for _ in range(num_transactions):
        customer = random.choice(customer_data)
        transaction = {
            'TransactionID': fake.unique.random_number(digits=8),
            'CustomerID': customer['CustomerID'],
            'TransactionAmount': round(random.uniform(10, 5000), 2),
            'TransactionDate': fake.date_time_this_year(),
            'Merchant': fake.company()
        }
        transactions.append(transaction)
    return transactions

# Generate 100 customer details
num_customers = 100
customer_data = generate_customer_data(num_customers)

# Generate 500 transaction records
num_transactions = 500
transaction_data = generate_transaction_data(num_transactions, customer_data)

# Convert data to pandas DataFrame for easier analysis
customers_df = pd.DataFrame(customer_data)
transactions_df = pd.DataFrame(transaction_data)

# Print sample data
print("Customer Details:")
print(customers_df.head())

print("\nTransaction Details:")
print(transactions_df.head())

customers_df.to_csv('customers_df.csv',index=False)
transactions_df.to_csv('transactions_df.csv',index=False)
