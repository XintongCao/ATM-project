import time
from Packages.viewClass import Views
from Packages.controllerClass import Controller
class Main():
    def __init__(self):
        #Instantiating the view-object
        view=Views()
        #Instantiating the operational control class
        obj=Controller()

        while True:
            #Allowing the user to select operational options
            num=input('Please select a function: ')
            #verify if user's input is correct
            code=['1','2','3','4','5','6','7','8','9','0']
            if num not in code:
                time.sleep(1)
                print('''
*********************************************
*                                           *
* Error in your input, please select again. *
*                                           *
*********************************************
''')
                view.showfunc()
                #Skip this loop
                continue
            #Process control
            if num=='1':
                obj.registration()
            elif num=='2':
                obj.enquiry()
            elif num=='3':
                obj.deposit()
            elif num=='4':
                obj.withdrawal()
            elif num=='5':
                obj.transfer()
            elif num=='6':
                obj.change_password()
            elif num=='7':
                obj.lockcard()
            elif num=='8':
                obj.unlockcard()
            elif num=='9':
                obj.replacecard()
            elif num=='0':
                obj.exit()
                break
if __name__=='__main__':
    Main()
