from flask import Flask
from src.systemInfo import SystemInformation

app = Flask(__name__)

@app.route("/", methods=["GET"])
def getSystemInfo():

    s = SystemInformation()

    return s.getSystemInfo()