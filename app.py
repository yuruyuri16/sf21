from flask import Flask
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

counter = 0
sleep_time = 120


@app.route('/rate-limit-me')
@limiter.limit('600/minute')
def rateLimit():
    return jsonify(Result="Rate-Limit-Success"), 200


@app.route('/throttle-me')
def throttle():
    global counter
    print(counter)
    if counter > 100:
        return jsonify(error="sleeping"), 503

    counter += 1

    if counter > 10:
        time.sleep(sleep_time)
        counter = 0
        return jsonify(error="woke up"), 503

    return jsonify(Result="Throttle-Limit-Success"), 200


if __name__ == "__main__":
    app.run(debug=True, port=7000)
