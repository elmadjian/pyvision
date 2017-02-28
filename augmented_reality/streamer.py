import zmq
import threading
import scipy.misc

class Streamer(threading.Thread):

    def __init__(self, address="127.0.0.1", port_img=5000, port_txt=5001):
        threading.Thread.__init__(self)
        context = zmq.Context()
        self.socket_img = context.socket(zmq.PUB)
        self.socket_txt = context.socket(zmq.PUB)
        self.socket_img.bind("tcp://"+address+":"+str(port_img))
        self.socket_txt.bind("tcp://"+address+":"+str(port_txt))


    def send_matrix(self, detected, matrix):
        message = {"type": "mat", "det": detected, "obj": matrix}
        self.socket_txt.send_json(message)


    def send_image(self, img):
        image = img.tobytes()
        self.socket_img.send(image)



if __name__=="__main__":
    streamer = Streamer()
    while True:
        teste = input("Type something to send: ")
        streamer.send_string(teste)
