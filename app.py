from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# ==================== CONFIGURATION ====================
SMTP_HOST = "smtp.office365.com"          # Microsoft 365  Official Host
SMTP_PORT = 587                           # Standard TLS Port
SENDER_EMAIL = "myatphonesan@cbbank.com.mm"         
SENDER_PASSWORD = "lhjfhknssnbqkczl"            # Outlook Password
RECEIVER_EMAIL = "ai.admin@cbbank.com.mm" 
# =======================================================


@app.route('/')
def home():
    return "Python Flask Server is Running Successfully!"

@app.route('/api/send-loan-email', methods=['POST']) 
def send_loan_email():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        staff_id = data.get('staffId')
        staff_name = data.get('staffName')
        position = data.get('position')
        department = data.get('department')
        nrc = data.get('nrc')
        father_name = data.get('fatherName')
        father_nrc = data.get('fatherNRC')
        address = data.get('address')
        phone = data.get('phone')
        salary = data.get('salary')
        loan_type = data.get('loanType')
        loan_amount = data.get('loanAmount')
        salary_multiple = data.get('salaryMultiple')
        account_no = data.get('accountNo')
        guarantor1_name = data.get('guarantor1Name')
        guarantor1_email = data.get('guarantor1Email')
        guarantor2_name = data.get('guarantor2Name')
        guarantor2_email = data.get('guarantor2Email')
        hod_name = data.get('hodName')
        hod_email = data.get('hodEmail')

        msg = MIMEMultipart()
        msg['From'] = f"CB Loan System <{SENDER_EMAIL}>"
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"ဝန်ထမ်းချေးငွေလျှောက်လွှာတင်ခြင်း - {staff_name} ({staff_id})"

        html_body = f"""
        <html>
        <body style="font-family: sans-serif; color: #333;">
            <h3 style="color: #0056b3;">ဝန်ထမ်းချေးငွေ လျှောက်လွှာအသစ် ရောက်ရှိလာပါသည်။</h3>
            <a href="https://many-phones-camp.loca.lt/" target="_blank">View Application</a>
            <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%; max-width: 600px; border-color: #d0d0d0;">
                <tr style="background-color: #f4f7f6;"><th colspan="2" style="text-align: left;">၁။ လျှောက်ထားသူ အချက်အလက်</th></tr>
                <tr><td><strong>ဝန်ထမ်း ID အမှတ်</strong></td><td>{staff_id}</td></tr>
                <tr><td><strong>အမည်</strong></td><td>{staff_name}</td></tr>
                <tr><td><strong>ရာထူး</strong></td><td>{position}</td></tr>
                <tr><td><strong>ဌာန (Division)</strong></td><td>{department}</td></tr>
                <tr><td><strong>မှတ်ပုံတင်အမှတ်</strong></td><td>{nrc}</td></tr>
                <tr><td><strong>အဖအမည် / မှတ်ပုံတင်</strong></td><td>{father_name} ({father_nrc})</td></tr>
                <tr><td><strong>အမြဲတမ်းနေရပ်လိပ်စာ</strong></td><td>{address}</td></tr>
                <tr><td><strong>ဖုန်းနံပါတ်</strong></td><td>{phone}</td></tr>
                <tr style="background-color: #f4f7f6;"><th colspan="2" style="text-align: left;">၂။ ချေးငွေဆိုင်ရာ အချက်အလက်</th></tr>
                <tr><td><strong>စုစုပေါင်းလစာ</strong></td><td>{salary} MMK</td></tr>
                <tr><td><strong>ချေးငွေအမျိုးအစား</strong></td><td>{loan_type}</td></tr>
                <tr><td><strong>ချေးလိုသောငွေပမာဏ</strong></td><td>{loan_amount} MMK</td></tr>
                <tr><td><strong>လစာဝင်ငွေ အဆ</strong></td><td>{salary_multiple}</td></tr>
                <tr><td><strong>CB BANK Account No.</strong></td><td>{account_no}</td></tr>
                <tr style="background-color: #f4f7f6;"><th colspan="2" style="text-align: left;">၃။ အာမခံသူများနှင့် တာဝန်ခံများ</th></tr>
                <tr><td><strong>အာမခံသူ (၁)</strong></td><td>{guarantor1_name} ({guarantor1_email})</td></tr>
                <tr><td><strong>အာမခံသူ (၂)</strong></td><td>{guarantor2_name} ({guarantor2_email})</td></tr>
                <tr><td><strong>HOD အမည် / Email</strong></td><td>{hod_name} ({hod_email})</td></tr>
            </table>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully!"}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)