app = Flask(__name__)

@app.route('/')
def index():
    return("Hahaha success")

if __name__ == '__main__':
      app.run()