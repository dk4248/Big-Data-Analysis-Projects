from train import train
from query_connector import connect

def main():
    print("Making the Database")
    train()
    print("Database made")
    print("Connecting to the Database")
    connect()
    print("Connected to the Database")

if __name__ == '__main__':
    main()

    

    