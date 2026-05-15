from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Social Media Automation</title>
        <style>
            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:100px;
            }
            h1{
                color:#38bdf8;
                font-size:50px;
            }
            p{
                font-size:22px;
            }
            .box{
                background:#1e293b;
                width:60%;
                margin:auto;
                padding:40px;
                border-radius:15px;
                box-shadow:0 0 20px rgba(0,0,0,0.4);
            }
        </style>
    </head>
    <body>

        <div class="box">
            <h1>AI Social Media Automation</h1>

            <p>
                Railway Deployment Successful
            </p>

            <p>
                Flask App Running Successfully
            </p>
        </div>

    </body>
    </html>
    """

@app.route("/health")
def health():
    return {
        "status": "success",
        "message": "Server Running"
    }

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )