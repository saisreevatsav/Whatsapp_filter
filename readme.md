# WhatsApp Web Job Filter

A Python automation tool to fetch messages from WhatsApp Web groups or channels, filter job-related messages, and log them into a daily Excel sheet.

---

## Features

- Open WhatsApp Web automatically in Microsoft Edge.
- Fetch messages from a specific group or channel.
- Filter messages containing job-related keywords like:
  `fresher, 2025, job, hiring, developer, software, intern, off-campus, walk-in, drive, placement`.
- Export filtered messages to an Excel file named by date (e.g., `whatsapp_job_updates_YYYY-MM-DD.xlsx`).
- Fetch messages only for the current day.

---

## Prerequisites

- Python 3.10+ (tested on 3.12)
- Microsoft Edge browser installed
- Edge WebDriver (`msedgedriver.exe`) corresponding to your Edge version
- Internet connection for WhatsApp Web and Selenium WebDriver

---

## Installation

1. Clone the repository or download the script:

```bash
git clone <repository_url>
cd Whatsapp_Filter

    Install the Python dependencies:

pip install -r requirements.txt

    Download Edge WebDriver:

    Visit Edge WebDriver

    Ensure the version matches your installed Edge browser.

    Place msedgedriver.exe in your project folder or update the path in filter.py:

driver_path = r"D:\Projects\Whatsapp_Filter\msedgedriver.exe"

Usage

    Run the script:

python filter.py

    Enter the group or channel name when prompted:

Enter the WhatsApp group/channel name: JOBS & VACANCIES 2025

    Open WhatsApp Web in Edge and scan the QR code if not logged in.

    The script will fetch messages from today, filter job-related messages, and save them to an Excel file.

Output

    Daily Excel file:

whatsapp_job_updates_YYYY-MM-DD.xlsx

Columns:

Sender	Message
Name	Text of the message