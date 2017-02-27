import zmq
import threading
import scipy.misc

class Streamer(threading.Thread):

    def __init__(self, address="127.0.0.1", port=5000):
        threading.Thread.__init__(self)
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://"+address+":"+str(port))

    def send_string(self, msg):
        self.socket.send_string(msg)

    def send_object(self, obj):
        self.socket.send_json(obj)

    def send_image(self, img):
        image = img.tobytes()
        self.socket.send(image)



if __name__=="__main__":
    streamer = Streamer()
    while True:
        teste = input("Type something to send: ")
        streamer.send_string(teste)
