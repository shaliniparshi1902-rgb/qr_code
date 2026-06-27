from __future__ import annotations

from pathlib import Path
from sys import path

import streamlit as st


BACKEND_DIR = Path(__file__).resolve().parent / "src" / "backend"
if str(BACKEND_DIR) not in path:
    path.insert(0, str(BACKEND_DIR))

from services.qr_generator import build_qr_content, generate_qr_bytes  # noqa: E402
from utils.validator import validate_payload  # noqa: E402


QR_TYPES = {
    "Text": "text",
    "Website URL": "url",
    "Contact": "contact",
    "Phone": "phone",
    "Email": "email",
    "SMS": "sms",
    "Address": "address",
    "Wi-Fi": "wifi",
    "UPI Payment": "upi",
    "Event": "event",
}


def main() -> None:
    """Render the Streamlit QR code generator."""
    st.set_page_config(page_title="QR Code Generator", layout="centered")
    st.title("QR Code Generator")
    st.caption("Generate downloadable PNG QR codes from text, links, contacts, Wi-Fi, UPI, and more.")

    selected_label = st.selectbox("QR code type", list(QR_TYPES))
    qr_type = QR_TYPES[selected_label]
    content = collect_content(qr_type)
    payload = {"type": qr_type, "content": content}

    if st.button("Generate QR Code", type="primary", use_container_width=True):
        is_valid, error = validate_payload(payload)
        if not is_valid:
            st.error(error)
            return

        qr_content = build_qr_content(qr_type, content)
        image_bytes = generate_qr_bytes(qr_content)

        st.success("QR code generated.")
        st.image(image_bytes, caption="Preview", use_container_width=False)
        st.download_button(
            "Download PNG",
            data=image_bytes,
            file_name=f"{qr_type}-qr-code.png",
            mime="image/png",
            use_container_width=True,
        )

        with st.expander("Encoded content"):
            st.code(qr_content)


def collect_content(qr_type: str) -> str | dict[str, str | bool]:
    """Collect Streamlit form fields for the selected QR type."""
    if qr_type == "contact":
        return {
            "name": st.text_input("Full name"),
            "phone": st.text_input("Phone number"),
            "email": st.text_input("Email address"),
            "address": st.text_area("Address", height=90),
        }
    if qr_type == "wifi":
        encryption = st.selectbox("Encryption", ["WPA", "WEP", "nopass"])
        return {
            "ssid": st.text_input("Network name"),
            "password": st.text_input("Password", type="password"),
            "encryption": encryption,
            "hidden": st.checkbox("Hidden network"),
        }
    if qr_type == "sms":
        return {
            "phone": st.text_input("Phone number"),
            "message": st.text_area("Message", height=100),
        }
    if qr_type == "upi":
        return {
            "upi_id": st.text_input("UPI ID"),
            "name": st.text_input("Payee name"),
            "amount": st.text_input("Amount"),
        }
    if qr_type == "event":
        start_date = st.date_input("Start date")
        start_time = st.time_input("Start time")
        end_date = st.date_input("End date")
        end_time = st.time_input("End time")
        return {
            "title": st.text_input("Event title"),
            "start": f"{start_date.isoformat()}T{start_time.isoformat()}",
            "end": f"{end_date.isoformat()}T{end_time.isoformat()}",
            "location": st.text_input("Location"),
            "description": st.text_area("Description", height=100),
        }

    labels = {
        "text": "Text",
        "url": "Website URL",
        "phone": "Phone number",
        "email": "Email address",
        "address": "Address",
    }
    return st.text_area(labels.get(qr_type, "Content"), height=120)


if __name__ == "__main__":
    main()
