import subprocess
subprocess.call('powershell')
subprocess.call("$env:FLASK_ENV='development'")
subprocess.call("$env:FLASK_APP='application.py'")
subprocess.call("flask run --host=0.0.0.0")
