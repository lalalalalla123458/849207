import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# 从GitHub读取邮箱信息
sender = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
receiver = sender

urls = {
    "深圳卫健委": "http://wjw.sz.gov.cn/xxgk/rsxx/",
    "深圳人社局": "http://hrss.sz.gov.cn/xxgk/zpgg/"
}

keywords = ["电镜", "实验", "技术", "检验", "事业编", "招聘"]

def get_jobs():
    results = []

    for name, url in urls.items():
        try:
            res = requests.get(url, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all("a"):
                text = link.get_text(strip=True)
                href = link.get("href")

                if any(k in text for k in keywords):
                    results.append(f"[{name}] {text}\n{href}")

        except Exception as e:
            results.append(f"{name} 抓取失败")

    return results


def send_email(content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "深圳招聘监控"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()


if __name__ == "__main__":
    jobs = get_jobs()

    if jobs:
        content = "\n\n".join(jobs)
    else:
        content = "今天没有新招聘"

    send_email(content)
