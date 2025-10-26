import time
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ---------------------------------------------
# 1️⃣ Configure WhatsApp Web Access (Edge)
# ---------------------------------------------
def open_whatsapp_edge():
    edge_options = Options()
    
    # Use a fresh user data folder for Edge automation
    edge_options.add_argument(r"--user-data-dir=D:\Projects\Whatsapp_Filter\edge_whatsapp_profile")
    
    # Safe automation flags
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--start-maximized")
    
    # 🔹 Use local EdgeDriver instead of downloading
    driver_path = r"D:\Projects\Whatsapp_Filter\msedgedriver.exe"  # <-- Update this path
    driver = webdriver.Edge(
        service=Service(driver_path),
        options=edge_options
    )
    
    driver.get("https://web.whatsapp.com/")
    print("📱 Please scan the QR code if required.")
    
    # Wait until WhatsApp chat list loads
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))
    )
    
    print("✅ WhatsApp Web loaded successfully!")
    return driver

# ---------------------------------------------
# 2️⃣ Fetch messages from a group/channel
# ---------------------------------------------
def fetch_whatsapp_messages(group_name):
    driver = open_whatsapp_edge()  # Use Edge function
    wait = WebDriverWait(driver, 20)

    print(f"🔍 Searching for '{group_name}' ...")

    # WhatsApp Web’s search box (updated XPaths)
    try:
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
    except:
        # fallback selector for newer versions
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@contenteditable='true'])[1]"))
        )

    search_box.clear()
    search_box.send_keys(group_name)
    time.sleep(2)

    # Click the first result
    group = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[@title='{group_name}']"))
    )
    group.click()
    print(f"📂 Opened group/channel: {group_name}")

    time.sleep(3)

    # Fetch all visible messages
    messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]")

    data = []
    for msg in messages:
        try:
            text = msg.find_element(By.XPATH, ".//span[contains(@class,'selectable-text')]").text
            timestamp = msg.find_element(By.XPATH, ".//div[contains(@class,'copyable-text')]").get_attribute("data-pre-plain-text")
            sender = re.findall(r'\[(.*?)\]', timestamp)
            sender = sender[0] if sender else "Unknown"
            data.append([sender, text])
        except:
            continue

    driver.quit()
    print(f"✅ Fetched {len(data)} messages.")
    return pd.DataFrame(data, columns=["Sender", "Message"])

# ---------------------------------------------
# 3️⃣ NLP Filtering of Job-related Messages
# ---------------------------------------------
def filter_messages(df):
    job_keywords = [
        "fresher", "2025", "job", "hiring", "developer",
        "software", "intern", "off-campus", "walk-in", "drive", "placement"
    ]

    regex_pattern = "|".join(job_keywords)
    filtered_df = df[df["Message"].str.contains(regex_pattern, case=False, na=False)]
    print(f"✅ Filtered {len(filtered_df)} relevant job messages.")
    return filtered_df

# ---------------------------------------------
# 4️⃣ Export to Excel (daily log)
# ---------------------------------------------
def save_to_excel(df):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"whatsapp_job_updates_{today}.xlsx"
    df.to_excel(filename, index=False)
    print(f"📊 Messages saved to '{filename}' successfully!")

# ---------------------------------------------
# 5️⃣ Main Routine
# ---------------------------------------------
def main():
    print("🚀 WhatsApp Web Job Filter Running...")
    group_name = input("Enter the WhatsApp group/channel name: ").strip()
    df = fetch_whatsapp_messages(group_name)
    filtered_df = filter_messages(df)
    save_to_excel(filtered_df)

if __name__ == "__main__":
    main()

