import time
from Packages.viewClass import Views
from Packages.controllerClass import Controller
class Main():
    def __init__(self):
        #实例化视图对象
        view=Views()
        #实例化操作控制类
        obj=Controller()

        while True:
            #让用户选择操作选项
            num=input('Please select a function: ')
            #需要验证用户的输入是否正确
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
                #跳过本次循环
                continue
            #以下是使用流程控制。也可以改成其他形式，例如，字典
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
