import throttle
from ndn.app import NDNApp
from ndn.security import KeychainDigest

app = NDNApp(face=None, keychain=KeychainDigest())


# limit to 25 calls per second
@throttle.wrap(1, 25)
def put_data(name, content, freshness_period):
    app.put_data(name, content=content, freshness_period=freshness_period)


@app.route('/hello/test')
def on_interest(name, interest_param, application_param):
    put_data(name, b'Content', 10000)


app.run_forever()
