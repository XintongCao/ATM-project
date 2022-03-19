import random, pickle,os
from Packages import cardClass as card
from Packages import userClass as user
#Operation Control Class
class Controller():
    #Data storage format
    userid_cardobj_dict=dict() #{User ID：Card object}
    cardid_userobj_dict=dict() #{Card number：User object}
    #url for data storage
    user_file_url='./Databases/user.txt'
    card_file_url='./Databases/card.txt'
    #1.Registration function
    def registration(self):
        #Obtain【user name】/【user ID】/【phone number】/【PIN】input by the user
        name=self.__getusername()
        userid=self.__getuserid()
        #Check if the current ID number already exists
        if userid in self.userid_cardobj_dict:
            print(f'''
*******************************************************
*                                                     *
* This userid already exists. Its card number: {self.userid_cardobj_dict[userid].cardid}. *
*                                                     *
*******************************************************
''')
            return
        phone_num=self.__getphone_num()
        pwd=self.__getpwd()
        print('Name:',name,' User_id:',userid,' Phone number:',phone_num,' Password:',pwd)

        #Create a bank card number
        cardid=random.randint(10000,99999)
        cardobj=card.Card(cardid,pwd,balance=0,islock=False)
        #Create a user object and bind it to the bank card
        userobj=user.User(name,userid,phone_num,cardobj)
        #Create the user information that needs to be saved. Data format is {user ID:cardobj},{cardid:userobj}
        self.userid_cardobj_dict[userid]=cardobj
        self.cardid_userobj_dict[cardid]=userobj
        #Complete the creation
        print(f'''
***************************************************
*                                                 *
* Congratulation, {name}! Registration success!      *
* Your card no.: {cardid}. Your account balance: ${cardobj.balance}. *
*                                                 *
***************************************************
''')
    #Get all user information
    def __init__(self):
        #Load all data information
        self.__loaddata()

    def __loaddata(self):
        #Checking the existence of documents
        if os.path.exists(self.card_file_url):
            #Read information
            with open(self.card_file_url,'rb') as fp:
                self.userid_cardobj_dict=pickle.load(fp)
                #print(self.userid_cardobj_dict)
        if os.path.exists(self.user_file_url):
            #Read data
            with open(self.user_file_url,'rb') as fp:
                self.cardid_userobj_dict=pickle.load(fp)

    #2.Enquiry function
    def enquiry(self):
        #Get the card number of the user
        cardid=int(input('Please enter your card number: '))
        #Check the existence of the card number
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #Get Card Object
        cardobj=self.cardid_userobj_dict[cardid].card
        #If present, enter the password
        if self.__checkpwd(cardobj):
            #Verify that the card is locked
            if cardobj.islock:
                print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                return
            else:
                #Get the current card balance information by card number
                print(f'''
*******************************************************
*                                                     *
* Your card number: {cardid}. Your account balance: ${cardobj.balance}. *
*                                                     *
*******************************************************
''')

    #3.Deposit function
    def deposit(self):
        #Get the user's card number
        cardid=int(input('Please enter your card number: '))
        #Verify the existence of the card number
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #Get Card Object
        cardobj=self.cardid_userobj_dict[cardid].card
        #If present, verify password
        if self.__checkpwd(cardobj):
            #Verify that the card is locked
            if cardobj.islock:
                print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                return
            else:
                #Get deposit amount
                deposit=int(input('Please enter your deposit amount: '))
                #The deposit amount cannot be less than 0
                if deposit<=0:
                    print('''
*********************************************************
*                                                       *
* Your deposit amount is incorrect, please re-enter it. *
*                                                       *
*********************************************************
''')
                elif deposit>0:
                    cardobj.balance=cardobj.balance+deposit
                    print(f'''
********************************************
*                                          *
* Congratulations, {self.cardid_userobj_dict[cardid].name}! Deposit success! *
* Your current account balance: ${cardobj.balance}.       *
*                                          *
********************************************
''')

    #4.Withdrawal function
    def withdrawal(self):
        #Obtain user card number
        cardid=int(input('Please enter your card number: '))
        #Verify that the card number entered exists
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #Get Card Object
        cardobj=self.cardid_userobj_dict[cardid].card
        #Verify password if card exists
        if self.__checkpwd(cardobj):
            #Verify that the card is locked
            if cardobj.islock:
                print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                return
            else:
                #Get the withdrawal amount
                withdrawal=int(input('Please enter your withdrawal amount: '))
                #The withdrawal amount cannot be greater than the existing balance on the card
                if withdrawal>cardobj.balance:
                    print('''
****************************
*                          *
* Wrong withdrawal amount! *
*                          *
****************************
''')
                elif withdrawal<=cardobj.balance:
                    cardobj.balance=cardobj.balance-withdrawal
                    print(f'''
***********************************************
*                                             *
* Congratulations, {self.cardid_userobj_dict[cardid].name}! Withdrawal success! *
* Your current account balance: ${cardobj.balance}.          *
*                                             *
***********************************************
''')

    #5.Transfer function
    def transfer(self):
        #Get the card number of the user
        cardid=int(input('Please enter your card number: '))
        #Verify that the card number entered for the transfer exists
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #Get the card number and name of the recipient
        cardid_recipient=int(input('Please enter the card number of the recipient: '))
        name_recipient=input('Please enter the name of the recipient: ')
        #Get Card Object
        cardobj=self.cardid_userobj_dict[cardid].card
        #Verify password if card exists
        if self.__checkpwd(cardobj):
            #Verify that the card is locked
            if cardobj.islock:
                print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                return
            else:
                #Get the transfer amount
                transfer=int(input('Please enter your transfer amount: '))
                #The amount transferred cannot be greater than the existing balance on the card
                if transfer>cardobj.balance:
                    print('''
**************************
*                        *
* Wrong transfer amount! *
*                        *
**************************
''')
                elif transfer<=cardobj.balance:
                    cardobj.balance=cardobj.balance-transfer
                    print(f'''
*************************************************************
*                                                           *
* Congratulations, {self.cardid_userobj_dict[cardid].name}! Transfer success!                 *
* The name of the recipient: {name_recipient}. The transfer amount: ${transfer}. *
* Your current account balance: ${cardobj.balance}.                         *
*                                                           *
*************************************************************
''')

    #6.Change password
    def change_password(self):
        #Obtain user card number
        cardid=int(input('Please enter your card number: '))
        #Verify the existence of the user's card number
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        while True:
            #Let the user choose to use 【user ID】 or 【original password】 to change the password
            num_pwd=input('''
***************************************
*                                     *
*  (1) Original password (2) User ID  *
*                                     *
***************************************

Please select the mode to change your password:
''')
            #Verify that the numbers entered by the user are correct
            code_pwd=['1','2']
            if num_pwd not in code_pwd:
                print('''
*********************************************
*                                           *
* Error in your input, please select again. *
*                                           *
*********************************************
''')
                #return
            if num_pwd=='1':
                #Select【Original Password】to change your password
                #Get the Card Object
                cardobj=self.cardid_userobj_dict[cardid].card
                #Verify original password first
                if self.__checkpwd(cardobj):
                    #Verify that the card is locked
                    if cardobj.islock:
                        print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                        return
                    else:
                        #Set a new password
                        newpwd=self.__getnewpwd(cardobj)
                        cardobj.pwd=newpwd
                        print(f'''
****************************************************
*                                                  *
* Congratulations, {self.cardid_userobj_dict[cardid].name}! Password change success! *
* Your new card password: {cardobj.pwd}.                       *
*                                                  *
****************************************************
''')
                        #Jump out of this loop
                        return
            if num_pwd=='2':
                #Select【User ID】to change your password
                #Get the User Object
                userobj=self.cardid_userobj_dict[cardid]
                #Verify user ID number first
                if self.__checkuserid(userobj):
                    #Get the Card Object
                    cardobj=userobj.card
                    #Verify that the card is locked
                    if cardobj.islock:
                        print('''
**********************************************************
*                                                        *
* Your card is currently locked, please unlock it first. *
*                                                        *
**********************************************************
''')
                        return
                    else:
                        #Set a new password
                        newpwd=self.__getnewpwd(cardobj)
                        cardobj.pwd=newpwd
                        print(f'''
****************************************************
*                                                  *
* Congratulations, {userobj.name}! Password change success! *
* Your new card password: {cardobj.pwd}.                       *
*                                                  *
****************************************************
''')
                        return
    #7.Card lock function
    def lockcard(self):
        print('Lock card ')
    #8.Card unlock function
    def unlockcard(self):
        print('Unlock card ')
    #9.Card replacement function
    def replacecard(self):
        print('Replace card ')
    #0.Exit
    def exit(self):
        #Write the current data, to a file
        with open(self.card_file_url,'wb+') as fp:
            pickle.dump(self.userid_cardobj_dict,fp)
        with open(self.user_file_url,'wb+') as fp:
            pickle.dump(self.cardid_userobj_dict,fp)
        print('''
****************
*              *
* Exit success *
*              *
****************
''')

    #Private method for obtaining a username
    def __getusername(self):
        while True:
            name=input('Please enter your name: ')
            if not name:
                print('The name you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return name
    #Private method for obtaining a user ID
    def __getuserid(self):
        while True:
            userid=int(input('Please enter your ID: '))
            if not userid:
                print('The ID you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return userid
    #Private method for obtaining a user's phone number
    def __getphone_num(self):
        while True:
            phone_num=int(input('Please enter your phone number: '))
            if not phone_num:
                print('The phone number you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return phone_num
    #Private method for obtaining the password
    def __getpwd(self):
        while True:
            pwd=int(input('Please enter your password: '))
            if not pwd:
                print('The password you have entered is incorrect, please re-enter it: ')
                continue
            else:
                #Once the password has been entered correctly, confirm the password again
                repwd=int(input('Please enter your password, again: '))
                if repwd==pwd:
                    return pwd
                else:
                    print('''
****************************************************************
*                                                              *
* The entered two passwords are different, please re-enter it. *
*                                                              *
****************************************************************
''')
                    continue

    #Private method for obtaining a new password
    def __getnewpwd(self,cardobj):
        while True:
            newpwd=int(input('Please enter your new password: '))
            if newpwd==cardobj.pwd:
                print('''
***********************************************************************************
*                                                                                 *
* Your new entered password is the same as your original one, please re-enter it. *
*                                                                                 *
***********************************************************************************
''')
                continue
            else:
                #Once the password has been entered correctly, confirm the password again
                renewpwd=int(input('Please enter your new password, again: '))
                if renewpwd==newpwd:
                    return newpwd
                else:
                    print('''
********************************************************************
*                                                                  *
* The new password twice entered is different, please re-enter it. *
*                                                                  *
********************************************************************
''')
                    continue

    #Check if the password is correct
    def __checkpwd(self,cardobj):
        num=3
        while True:
            #Obtain the PIN
            pwd=int(input('Please enter your password: '))
            #Check if the password is correct
            if pwd==cardobj.pwd:
                return True
            else:
                num=num-1
                if num==0:
                    #card lock
                    cardobj.islock=True
                    print('''
************************
*                      *
* Your card is locked. *
*                      *
************************
''')
                    break
                else:
                    print(f'''
**************************************************
*                                                *
* Wrong password, you have {num} attempts remaining. *
*                                                *
**************************************************
''')

    #Check if the user ID card is correct
    def __checkuserid(self,userobj):
        while True:
            #Obtain user ID
            userid=int(input('Please enter your user ID number: '))
            #Check if the ID number is correct
            if userid==userobj.userid:
                return True
            else:
                #Card lock
                self.userobj.card.islock=True
                print('''
***************************************
*                                     *
* Wrong user ID, your card is locked. *
*                                     *
***************************************
''')
                break
