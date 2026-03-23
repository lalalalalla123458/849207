import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# 邮箱
sender = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
receiver = sender

# 网站（加回丁香园）
urls = {
    "高校人才网": "https://www.gaoxiaojob.com/zhaopin/",
    "丁香园": "https://www.jobmd.cn/jobs/all"
}

# 关键词（你的定制版）
keywords = [
    "电镜",
    "电子显微镜",
    "结构生物学",
    "结构解析",
    "cryo",
    "冷冻电镜",
    "蛋白纯化",
    "蛋白表达",
    "蛋白互作",
    "晶体学",
    "X-ray",
    "科研平台",
    "实验技术",
    "技术员",
    "事业编",
    "医院",
    "科研"
]

def get_jobs():
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for name, url in urls.items():
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all("a"):
                text = link.get_text(strip=True)
                href = link.get("href")

                if text and any(k.lower() in text.lower() for k in keywords):
                    if href and not href.startswith("http"):
                        href = url + href

                    results.append(f"[{name}] {text}\n{href}")

        except Exception:
            # ❗关键：丁香园失败也不会影响整体
            results.append(f"{name} 抓取失败（正常，可忽略）")

    return results


def send_email(content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "深圳招聘监控（结构生物学方向）"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        print("邮件发送失败:", e)


if __name__ == "__main__":
    jobs = get_jobs()

    if jobs:
        jobs = list(set(jobs))
        content = "\n\n".join(jobs[:30])
    else:
        content = "今天没有符合条件的新招聘"

    send_email(content)
