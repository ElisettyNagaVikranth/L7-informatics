# L7-informatics

# Expense Tracker CLI App (with Budget Alerts)

A simple Python-based command-line expense tracker that allows users to log expenses, set monthly budgets, and view spending summaries. Data is stored in a per-user JSON file and optionally exportable to CSV (soon). You can also run it in a Docker container.

# Project Structure
L7-informatics/
├── README.md    
├── L7 infromatics/          
│   ├── Expense.py 
│   └── Dockerfile         

## Features

- Log daily expenses with category and description
- Set monthly budgets per category
- View total monthly spending
- View spending by category
- Compare spending vs. budget with alerts
- JSON-based data persistence
- Docker support for easy deployment


## Steps for implementation

### 1. Clone the Repository

git clone https://github.com/ElisettyNagaVikranth/L7-informatics.git
cd L7-informatics/L7 infromatics

### 2. Install the Python and the Docker

install the python 3.8 which is suitable.

### 3. Run the Application

python Expense.py

### 4.Docker Usage

1. Bulid the Docker Image
   docker build -t expense-tracker .

2. Run the Container
   docker run -it --rm expense-tracker

## File Descriptions
- Expense.py Main application logic
- Dockerfile: Containerizes the app

