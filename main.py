from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    print("hohoo")
    return("Hahaha success")

if __name__ == '__main__':
      app.run()