import time
from PyQt6.QtCore import QObject, pyqtSignal
import pywhatkit
import pyautogui

class WhatsAppSender(QObject):
    message_sent = pyqtSignal(str, bool)

    def __init__(self, web_view):
        super().__init__()
        self.web_view = web_view

    def send_whatsapp_message(self, number, message, attachments):
        js_code = f"""
        (async () => {{
            const number = "{number}";
            const message = `{message}`;
            const attachments = {attachments};
            
            // Open chat
            window.location.href = `https://web.whatsapp.com/send?phone=${{number}}&text=${{encodeURIComponent(message)}}`;
            
            // Wait for chat to load
            await new Promise(resolve => setTimeout(resolve, 5000));
            
            // Send message
            const sendButton = document.querySelector('button[data-testid="compose-btn-send"]');
            if (sendButton) {{
                sendButton.click();
                return "Message sent successfully";
            }} else {{
                return "Failed to send message";
            }}
        }})();
        """
        
        self.web_view.page().runJavaScript(js_code, self.handle_result)

    def handle_result(self, result):
        success = "successfully" in result.lower()
        self.message_sent.emit(result, success)

def format_phone_number(number):
    # Remove any non-digit characters
    cleaned_number = ''.join(filter(str.isdigit, number))
    
    # If the number doesn't start with '+' or '00', assume it's an Indian number and add the country code
    if not cleaned_number.startswith(('91', '00', '+')):
        cleaned_number = '91' + cleaned_number
    
    # Ensure the number starts with '+'
    if not cleaned_number.startswith('+'):
        cleaned_number = '+' + cleaned_number
    
    return cleaned_number

def send_whatsapp_message(number, message, attachments):
    try:
        formatted_number = format_phone_number(number)
        print(f"Sending message to formatted number: {formatted_number}")
        
        pywhatkit.sendwhatmsg_instantly(formatted_number, message, wait_time=15, tab_close=True)
        time.sleep(5)  # Wait for the message to be sent

        # Send attachments
        for attachment in attachments:
            pywhatkit.sendwhats_image(formatted_number, attachment, wait_time=15, tab_close=True)
            time.sleep(5)  # Wait for the attachment to be sent

        print(f"Message and attachments sent to {formatted_number}")
        return True, "Message and attachments sent successfully"
    except Exception as e:
        return False, f"Error sending message: {str(e)}"
