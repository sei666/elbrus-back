#~elbrus-back/run.py

from app import app

app.run(debug = False, host='0.0.0.0', port=5001)