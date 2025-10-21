import cv2
import numpy as np
import os
import time
from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time
import csv


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0
names = ['None', 'Ananthu','Kiran','Sreejith','vishwin']
cam = cv2.VideoCapture(0)
cam.set(3, 640) 
cam.set(4, 480) 
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

#lcd
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32],numbering_mode=GPIO.BOARD)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

votedList=['None']

def startCamera():
    ret, img =cam.read()
    cv2.imshow('Output',img)
    cv2.putText(img,'Face the Camera',(50,250),font,1,(255,255,255),2)
    k = cv2.waitKey(30) & 0xff
    if k==27:
       print('camera stoppped')
def buzz():
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(11,GPIO.LOW)

def vote():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
	
    # field names
    fields = ['LDF', 'UDF', 'BJP', 'NOTA']    
    filename = "vote.csv"
	
    # writing to csv file
    with open(filename, 'a') as csvfile:
	# creating a csv writer object
            csvwriter = csv.writer(csvfile)
		
            # writing the fields
            #csvwriter.writerow(fields)
		
	# writing the data rows
##            csvwriter.writerows(['0001'])
            
    while True:
        if (GPIO.input(8) == GPIO.LOW and GPIO.input(10) == GPIO.HIGH and GPIO.input(3) == GPIO.HIGH and GPIO.input(5) == GPIO.HIGH):
             with open(filename, 'a') as csvfile:
                 csvwriter = csv.writer(csvfile)   
                 csvwriter.writerows(['1000'])
             buzz()
             time.sleep(3)
             print('switch 1')
             lcd.clear()
             lcd.write_string('successfully votted')
             time.sleep(2)
             break


        elif (GPIO.input(8) == GPIO.HIGH and GPIO.input(10) == GPIO.LOW and GPIO.input(3) == GPIO.HIGH and GPIO.input(5) == GPIO.HIGH):
            with open(filename, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(['0100'])
            buzz()
            time.sleep(3)
            print('switch 2')
            lcd.clear()
            lcd.write_string('successfully votted')
            time.sleep(2)
            break


        elif (GPIO.input(8) == GPIO.HIGH and GPIO.input(10) == GPIO.HIGH and GPIO.input(3) == GPIO.LOW and GPIO.input(5) == GPIO.HIGH):
            print('switch 3')
            with open(filename, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(['0010'])
            buzz()
            time.sleep(3)
            print('switch 3')
            lcd.clear()
            lcd.write_string('successfully votted')
            time.sleep(2)
            break


        elif (GPIO.input(8) == GPIO.HIGH and GPIO.input(10) == GPIO.HIGH and GPIO.input(3) == GPIO.HIGH and GPIO.input(5) == GPIO.LOW):
            with open(filename, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(['0001'])
            buzz()
            time.sleep(3)
            print('switch 4')
            lcd.clear()
            lcd.write_string('successfully votted')
            time.sleep(2)
            break
    main()
            

def iden():
    lcd.clear()
    lcd.write_string('Helloo...!')
    time.sleep(2)
    lcd.clear()
    lcd.write_string('Welcome')
    time.sleep(2)
    lcd.clear()     
    lcd.write_string('Detecting Face...')
    print('sample running')
    for i in range(20):
        startCamera()    
        time.sleep(0.5)
    lcd.clear()
#IDENTIFICATION
    facecheckingCount=0
    while True:        
        print('start capture')
        ret, img =cam.read()    
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:        
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)        
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])  
       
            if (confidence < 60):
                facecheckingCount=facecheckingCount+1
                print(facecheckingCount)
                if(facecheckingCount>10):
                    facecheckingCount=0
                    if names[id] in votedList:
                        print('you have already votted')
                        lcd.clear()
                        lcd.write_string('YOU HAVE ALREADY VOTTED')
                        cv2.destroyAllWindows()
                        time.sleep(2)
                        lcd.clear()
                        main()
                    else:
                        votedList.append(names[id])
                        id = names[id]            
                        #print(confidence)
                        confidence = "  {0}%".format(round(100 - confidence))
                        lcd.clear()
                        lcd.write_string('you are allowed to vote')  
                        print(' you are allowed to vote')
                        cv2.destroyAllWindows()
                        vote()
                        time.sleep(2)
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
            cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
            cv2.imshow('Output',img)
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break


#vote()





def main():
    print('press button to start')
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True: # Run forever
        if GPIO.input(7) == GPIO.LOW:
            print("Button was pushed!")
            buzz()
            time.sleep(2)
            iden()

if __name__ == "__main__":
    main()

    
        
        
        
        
    

    

