import time
import RPi.GPIO as GPIO

G_PIN = 3 
B_PIN = 5
Y_PIN = 7
R_PIN = 11
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)

GPIO.setup(COUNTER_PIN, GPIO.IN)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)
GPIO.setup(Y_PIN, GPIO.OUT)
GPIO.setup(R_PIN, GPIO.OUT)

binary_bit3 = 0
binary_bit2 = 0
binary_bit1 = 0
binary_bit0 = 0

Flag = 0

def LedOutput():
    if binary_bit0 == 1:
        GPIO.output(R_PIN, GPIO.HIGH)
    if binary_bit0 == 0:
        GPIO.output(R_PIN, GPIO.LOW)
    if binary_bit1 == 1:
        GPIO.output(Y_PIN, GPIO.HIGH)
    if binary_bit1 == 0:
        GPIO.output(Y_PIN, GPIO.LOW)
    if binary_bit2 == 1:
        GPIO.output(B_PIN, GPIO.HIGH)
    if binary_bit2 == 0:
        GPIO.output(B_PIN, GPIO.LOW)
    if binary_bit3 == 1:
        GPIO.output(G_PIN, GPIO.HIGH)
    if binary_bit3 == 0:
        GPIO.output(G_PIN, GPIO.LOW)

try:
    while True:
        if GPIO.input(COUNTER_PIN) == GPIO.HIGH:
            binary_bit0 += 1
            print(1)

            if binary_bit0 == 2:
                binary_bit1 += 1
                binary_bit0 = 0
                print(2)

                if binary_bit1 == 2:
                    binary_bit2 += 1
                    binary_bit1 = 0
                    print(3)

                    if binary_bit2 == 2:
                        binary_bit3 += 1
                        binary_bit2 =0
                        print(4)

                        if binary_bit3 == 2:
                            binary_bit0 = 0
                            binary_bit1 = 0
                            binary_bit2 = 0
                            binary_bit3 = 0
                            print(5)
            LedOutput()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("kb")
finally:
    GPIO.cleanup()
    
