import time
class Views():

    def __init__(self):
        self.__showindex()
        print('System is loading, please wait...')
        time.sleep(1)
        self.showfunc()

    #Show Welcome screen
    def __showindex(self):
        varstr='''
************************************************
*                                              *
*                                              *
*              Welcome to Our Bank             *
*                                              *
*                                              *
************************************************
'''
        print(varstr)

    #Show Operation interface
    def showfunc(self):
        varstr='''
************************************************
*                                              *
*       (1)Registration    (2)Enquiry          *
*       (3)Deposit         (4)Withdrawal       *
*       (5)Transfer        (6)Change password  *
*       (7)Lock card       (8)Unlock card      *
*       (9)Replace card    (0)Exit             *
*                                              *
************************************************
'''
        print(varstr)

if __name__=='__main__':
    Views()
