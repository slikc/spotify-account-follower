import threading
from main import main
counter = 0

threads = int(input("How many threads do you want to run? "))

def thread_starter():
    global counter
    main()
    counter += 1
    
while True:
    if threading.active_count() <= threads:
        try:
            threading.Thread(target = thread_starter).start()
            print("Thread started. Total threads: " + str(threading.active_count()))
        except:
            pass
