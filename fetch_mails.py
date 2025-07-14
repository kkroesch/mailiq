import mailbox, json
from tqdm import tqdm
from email.header import decode_header

def decode_maybe(h):
    if h is None:
        return ""
    parts = decode_header(h)
    return "".join([
        (part.decode(enc or "utf-8", errors="ignore") if isinstance(part, bytes) else part)
        for part, enc in parts
    ])

def extract_body(msg):
    try:
        if msg.is_multipart():
            parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        parts.append(part.get_payload(decode=True).decode(errors="ignore"))
                    except Exception:
                        continue
            return "\n".join(parts)
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode(errors="ignore")
    except Exception:
        pass
    return ""

mbox = mailbox.mbox("/var/home/karsten/.var/app/org.mozilla.Thunderbird/.thunderbird/xwkrkrkt.default-esr/ImapMail/imap.mail.me.com/INBOX")
mails = []
errors = []

for msg in tqdm(mbox, desc="Mails verarbeiten"):
    try:
        mails.append({
            "id": str(msg.get("message-id") or ""),
            "from": decode_maybe(msg.get("from")),
            "to": decode_maybe(msg.get("to")),
            "subject": decode_maybe(msg.get("subject")),
            "date": str(msg.get("date") or ""),
            "body": extract_body(msg)
        })
    except Exception as e:
        errors.append(f"Fehler bei Mail: {str(e)}.")

with open("mails.json", "w") as f:
    json.dump(mails, f, indent=2)


print(errors)
