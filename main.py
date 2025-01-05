from multiprocessing import Process


from flask import Flask, render_template

def webserver():
    app = Flask(__name__)

    @app.route('/')
    def whoisusingmygpu():
        return render_template('index.html')

    app.run(debug=True)


def monitor_pool():
    print("TODO:")
    return

if __name__ == "__main__":
    ws = Process(target=webserver)
    mp = Process(target=monitor_pool)
    ws.start()
    mp.start()
    
