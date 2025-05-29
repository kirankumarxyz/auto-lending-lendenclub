import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()
# Constants
URL_FETCH = "https://investor-api.lendenclub.com/api/ims/retail-investor/v5/web/available-loans"
URL_LEND = "https://investor-api.lendenclub.com/api/ims/retail-investor/v5/web/bulk-lending"
URL_BAL = "https://investor-api.lendenclub.com/api/ios/retail-investor/v5/web/account-status?investor_id=1Z2F4Z8J1X&partner_code=LDC&partner_id="
HEADERS = {
    "authorization": os.getenv("LEN_DEN_AUTH"),
    "x-ldc-key": os.getenv("LEN_DEN_KEY"),
    "Content-Type": "application/json"
}

INVESTOR_ID = os.getenv("LEN_DEN_INVESTOR_ID")
BODY_FETCH = {
    "filters": ["tenure_5M","tenure_4M","tenure_3M","tenure_2M"],
    "sort_by": ["roi_high_low", "tenure_low_high"],
    "partner_code": "LDC",
    "investor_id": INVESTOR_ID,
    "partner_id": "",
    "limit": 10,
    "offset": 0,
    "loan_ids": []
}
def limit_array(arr, limit=10):
    return arr[:limit] if len(arr) > limit else arr

def fetch_loans():
    response = requests.post(URL_FETCH, headers=HEADERS, json=BODY_FETCH)
      # Debugging line to see the response content
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch loans:", response.status_code)
        return None
def fetch_balance():
    response = requests.get(URL_BAL, headers=HEADERS)
      # Debugging line to see the response content
    # print("response content:", response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch balance:", response.status_code)
        return None
def lend_to_loans(loan_roi_data):
    body = {
        "partner_code": "LDC",
        "investor_id": INVESTOR_ID,
        "loan_roi_data": loan_roi_data,
        "lending_amount": 250
    }
    print("Lending to loans:", loan_roi_data)
    response = requests.post(URL_LEND, headers=HEADERS, json=body)
    # print(response.text)
    if response.status_code == 200 and response.json().get("success")== 1:
        print("Successfully lent to loans:", loan_roi_data)
    else:
        print("Lending failed:", response.status_code, response.json().get("message", "No message in response"))

def run():
    # while True:
    print("Checking for eligible loans...")
    data = fetch_loans()
    # print(data)
    if data and data.get("success") == 1:
        loans = data["data"]["available_loans_list"]
        to_lend = []
        for loan in loans:
            try:
                roi = float(loan["loan_roi"])
                if roi >= 48:
                    to_lend.append({
                        "loan_id": loan["loan_id"],
                        "loan_roi": "{:.2f}".format(roi)
                    })
            except Exception as e:
                print("Error processing loan:", e)
        bal_json = fetch_balance()
        if bal_json and bal_json.get("success") == 1:
            balance = bal_json["data"].get("account_balance", 0)
            # print(bal_json)
            print(f"Current balance: {balance}")
            if balance < 250:
                print("Insufficient balance to lend. Waiting for next cycle.")
        # if to_lend and balance >= 250:
        print(len(to_lend), "loans found with ROI > 48.")
        max_nunber_of_loans_to_lend = int(balance // 250)
        print(f"Max number of loans to lend based on balance: {max_nunber_of_loans_to_lend}")
        if balance >= 250 and len(to_lend) > 0:
            lend_to_loans(limit_array(to_lend, max_nunber_of_loans_to_lend))
        else:
            print("No loans found with ROI > 48 or Balance is < 250.")
    else:
        print("No data returned or error from API.")

    # print("Sleeping for 15 minutes...\n")
    # time.sleep(900)  # Sleep for 900 seconds (15 minutes)

if __name__ == "__main__":
    run()
