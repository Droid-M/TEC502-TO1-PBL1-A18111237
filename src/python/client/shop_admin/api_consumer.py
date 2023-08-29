from helpers import file

if (file.env("ENV") == "SIMULATION"):
    cashiers = [
        {"id": 1, "situation": "FREE", }
    ]
    def get_cashiers_info():
        for i in cashiers:
            print(i)