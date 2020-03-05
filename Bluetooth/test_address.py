from bt_rssi import BluetoothRSSI
import time
import sys
import threading

# BT_ADDR = 'F4:F5:DB:98:33:E4'  # You can put your Bluetooth address here
NUM_LOOP = 3
lock = True

# def print_usage():
#     print("Usage: python test_address.py <bluetooth-address> [number-of-requests]")

def lock_unlock_protocol(BT_ADDR):
    global lock
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    elif BT_ADDR:
        addr = BT_ADDR
    else:
        print_usage()
        return
    if len(sys.argv) == 3:
        num = int(sys.argv[2])
    else:
        num = NUM_LOOP
    btrssi = BluetoothRSSI(addr=addr)
    avg_rssi = 0;
    for i in range(0, num):
        temp = btrssi.get_rssi()
        
        if(temp ==  None):
            temp = -100
        # print(temp)
        avg_rssi = avg_rssi + temp
        time.sleep(0.1)

    if(lock==True and (avg_rssi/NUM_LOOP)>-5):
        lock = False
        print("Unlock") #Model detect a registered device, so that out system will be unlocked 
        print(BT_ADDR)
        # time.sleep(5)
    elif(lock == False and (avg_rssi/NUM_LOOP)<-5):
        lock = True
        print("lock") #Model didn't detect any registered device, so that out system will be locked
        print(BT_ADDR)
        # time.sleep(5)

def main():
    addr1 = "F4:F5:DB:98:33:E4" #MAC address of one registered device
    addr2 = "20:34:FB:54:19:D8" #MAC address of another registered device
    while True:
        #Create two thread that will execute in parallal
        t1 = threading.Thread(target=lock_unlock_protocol, args=(addr1,))
        t2 = threading.Thread(target=lock_unlock_protocol, args=(addr2,))

        #Both threads are executing
        t1.start()
        t2.start()

        #Join the thread
        t1.join()
        # print("P1 done")
        t2.join()
        # print("P2 done")
        # lock_unlock_protocol()

if __name__ == '__main__':
    main()