import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()
# Constants
INVESTOR_ID = os.getenv("LEN_DEN_INVESTOR_ID")
URL_FETCH = "https://investor-api.lendenclub.com/api/ims/retail-investor/v5/web/available-loans"
URL_LEND = "https://investor-api.lendenclub.com/api/ims/retail-investor/v5/web/bulk-lending"
URL_BAL = f"https://investor-api.lendenclub.com/api/ios/retail-investor/v5/web/account-status?investor_id={INVESTOR_ID}&partner_code=LDC&partner_id="
HEADERS = {
    "authorization": os.getenv("LEN_DEN_AUTH"),
    "x-ldc-key": os.getenv("LEN_DEN_KEY"),
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}
# Headers for authentication
GIT_KEY = os.getenv("LEN_DEN_GIT_ISSUE_KEY")
try:
    LENDER_INTEREST_RATE_INNER = float(os.getenv("LENDER_INTEREST_RATE", "48"))
except (TypeError, ValueError):
    print("Warning: Invalid LENDER_INTEREST_RATE, defaulting to 48.")
    LENDER_INTEREST_RATE_INNER = 48.0
GITHUB_HEADERS = {
    "Authorization": f"token {GIT_KEY}",
    "Accept": "application/vnd.github.v3+json"
}

BODY_FETCH = {
    "filters": ["tenure_2M"],
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
    # print("response content:", response.text)
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
def lend_to_loans(loan_roi_data,loans_lent,balance):
    body = {
        "partner_code": "LDC",
        "investor_id": INVESTOR_ID,
        "loan_roi_data": loan_roi_data,
        "lending_amount": 250
    }
    print("Lending to loans:", loan_roi_data)
    response = requests.post(URL_LEND, headers=HEADERS, json=body)
    # print(response.text)
    new_bal_json = fetch_balance()
    if new_bal_json and new_bal_json.get("success") == 1:
        new_balance = new_bal_json["data"].get("account_balance", 0)
    if response.status_code == 200 and response.json().get("success")== 1:
        print("Successfully lent to loans:", loan_roi_data)
        create_github_issue(f"✅ Lending Success : {loans_lent} loans", f"Balance before {balance} \nBalance after {new_balance} \nLent to loans: {loan_roi_data}")
    else:
        tmp_response = response.json().get("message", "No message in response")
        print("Lending failed:", response.status_code, tmp_response)
        create_github_issue(f"❌ Lending Failed : {loans_lent} loans", f"Balance before {balance} \nBalance after {new_balance} \nResponse messgae {tmp_response}\nLent to loans: {loan_roi_data}")


# def check_condition():
#     # Dummy condition logic
#     return True

# def generate_output():
#     # This could be any logic
#     return "This is the function output which will go into the GitHub issue."

def create_github_issue(title, body):
    url = f"https://api.github.com/repos/{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}/issues"
    payload = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=GITHUB_HEADERS, json=payload)

    if response.status_code == 201:
        print("✅ Issue created successfully.")
    else:
        print(f"❌ Failed to create issue: {response.status_code}")
        print(response.json())

# Main logic
# if check_condition():
#     output = generate_output()
#     create_github_issue("Auto-generated issue from function output", output)
def run():
    bal_json = fetch_balance()
    if bal_json and bal_json.get("success") == 1:
        balance = bal_json["data"].get("account_balance", 0)
        # print(bal_json)
        print(f"Current balance: {balance}")
        if balance < 250:
            print("Insufficient balance to lend. Waiting for next cycle.")
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
                if roi >= LENDER_INTEREST_RATE_INNER:
                    to_lend.append({
                        "loan_id": loan["loan_id"],
                        "loan_roi": "{:.2f}".format(roi)
                    })
            except Exception as e:
                print("Error processing loan:", e)

        # if to_lend and balance >= 250:
        print(len(to_lend), f"loans found with ROI > {LENDER_INTEREST_RATE_INNER}.")
        max_nunber_of_loans_to_lend = int(balance // 250)
        print(f"Max number of loans to lend based on balance: {max_nunber_of_loans_to_lend}")
        if balance >= 250 and len(to_lend) > 0:
            lend_to_loans(limit_array(to_lend, max_nunber_of_loans_to_lend),len(limit_array(to_lend, max_nunber_of_loans_to_lend)),balance)
        else:
            print(f"No loans found with ROI > {LENDER_INTEREST_RATE_INNER} or Balance is < 250.")
    else:
        print("No data returned or error from API.")

    # print("Sleeping for 15 minutes...\n")
    # time.sleep(900)  # Sleep for 900 seconds (15 minutes)

if __name__ == "__main__":
    run()
