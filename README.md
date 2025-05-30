# 💸 Auto Lending Bot for LenDenClub

This Python script automates lending to high-interest loans on [LenDenClub](https://www.lendenclub.com/) using their investor API. It fetches available loans every 15 minutes via GitHub Actions, filters for loans with ROI ≥ 48%, and attempts to lend ₹250 to each — provided the investor's account has sufficient balance.

---

## 📌 Features

- ✅ Automatically fetches available loans every 15 minutes
- ✅ Filters loans based on ROI (≥ 48%)
- ✅ Lends ₹250 per eligible loan, up to available account balance
- ✅ Logs success and errors along with git issue creation
- ✅ Hosted on GitHub Actions (runs in the cloud, no local execution required)

---

## 🛠️ Technologies Used

- Python 3
- `requests` library
- GitHub Actions (for scheduling)

---

## 🧠 How It Works

1. **Fetch Loans:** Uses LenDenClub API to fetch loans with filters like tenure and ROI.
2. **Filter & Decide:** Selects loans with ROI ≥ 48%.
3. **Check Balance:** Ensures minimum ₹250 balance is available.
4. **Lend:** Sends a lending request using bulk lending API.
5. **Create Git Issue:** Log the result by creating a GitHub issue for success/failure
6. **Wait:** Repeats every 15 minutes via scheduled GitHub workflow.

---

## 🚀 Setup (Optional for Local Use)

> You don't need to run this locally if you're using GitHub Actions. But for testing:

### 1. Clone the Repository
```bash
git clone https://github.com/pkalyankumar1010/auto-lending-lendenclub.git
cd auto-lending-lendenclub
```
### 2.Install Dependencies
```bash 
pip install requests dotenv
```
### 3.🔐 Environment Variables
```bash
# .env file
# LenDenClub API Auth
LEN_DEN_AUTH=your_auth_token
LEN_DEN_KEY=your_ldc_key
LEN_DEN_INVESTOR_ID=your_investor_id

# GitHub API Auth (for creating issues)
LEN_DEN_GIT_ISSUE_KEY=your_github_token
REPO_OWNER=your_github_username
REPO_NAME=your_repository_name
```
### 4.Run the Script
```bash
python auto_lender.py
```

## 🕒 GitHub Actions Schedule
The automation is set to run every 15 minutes using GitHub Actions.
See .github/workflows/lend-cron.yml:
```yml
on:
  schedule:
    - cron: "*/15 * * * *"
```

## 🔐 API Token & Headers
- The script uses a hardcoded API token and headers, which are specific to your LenDenClub account.
- **Make sure to keep your tokens private and never share your token publicly.**
To rotate or update tokens:
- Edit the HEADERS dictionary in auto_lender.py.


## ❓ Q&A
- Dont foget to env varibales (auth token , xldc key , investor id) as secrets in github repo settings also in lend-cron.yml in github/workflows
- Create a token at [PAT](https://github.com/settings/personal-access-tokens) with repo R/W issues
- if github action doesnot start
    - Check GitHub Actions settings
    - Go to:
        - Repository → Settings → Actions → General

    - Ensure:
        - "Allow all actions and reusable workflows" is selected.

    - Under Workflow permissions, check:
        - ✅ "Read and write permissions" is selected.
        - ✅ "Allow GitHub Actions to create and approve pull requests" is enabled (optional).
## 🔮 Future 
- 📅 if lending is sucess or fail create a github issue

## 👤 Author
Kalyan
🛠 EDA Engineer | 💡 Automation Enthusiast
Feel free to connect or contribute ideas!