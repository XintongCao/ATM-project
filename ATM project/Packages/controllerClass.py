import random, pickle,os
from Packages import cardClass as card
from Packages import userClass as user
#操作控制类
class Controller():
    #数据存储格式
    userid_cardobj_dict=dict() #{身份证ID：银行卡对象}
    cardid_userobj_dict=dict() #{银行卡ID：用户对象}
    #数据存储的url
    user_file_url='./Databases/user.txt'
    card_file_url='./Databases/card.txt'
    #1.注册功能
    def registration(self):
        #获取用户输入的【用户名】/【身份证号】/【手机号】/【密码】
        name=self.__getusername()
        userid=self.__getuserid()
        #检测当前身份证号 是否已经存在
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

        #创建一个银行卡号
        cardid=random.randint(10000,99999)
        cardobj=card.Card(cardid,pwd,balance=0,islock=False)
        #创建用户对象，和银行卡进行绑定
        userobj=user.User(name,userid,phone_num,cardobj)
        #创建需要保存用户信息 数据格式{身份证号：cardobj},{cardid:userobj}
        self.userid_cardobj_dict[userid]=cardobj
        self.cardid_userobj_dict[cardid]=userobj
        #完成创建
        print(f'''
***************************************************
*                                                 *
* Congratulation, {name}! Registration success!      *
* Your card no.: {cardid}. Your account balance: ${cardobj.balance}. *
*                                                 *
***************************************************
''')
    #获取所有的用户信息
    def __init__(self):
        #加载所有数据信息
        self.__loaddata()

    def __loaddata(self):
        #检验文件是否存在
        if os.path.exists(self.card_file_url):
            #读取数据
            with open(self.card_file_url,'rb') as fp:
                self.userid_cardobj_dict=pickle.load(fp)
                #print(self.userid_cardobj_dict)
        if os.path.exists(self.user_file_url):
            #读取数据
            with open(self.user_file_url,'rb') as fp:
                self.cardid_userobj_dict=pickle.load(fp)

    #2.查询功能
    def enquiry(self):
        #获取用户数据的卡号
        cardid=int(input('Please enter your card number: '))
        #验证卡号是否存在
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #获取卡对象
        cardobj=self.cardid_userobj_dict[cardid].card
        #如果存在，则输入密码
        if self.__checkpwd(cardobj):
            #验证是否锁卡
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
                #通过卡号获取当前卡的余额信息
                print(f'''
*******************************************************
*                                                     *
* Your card number: {cardid}. Your account balance: ${cardobj.balance}. *
*                                                     *
*******************************************************
''')

    #3.存款功能
    def deposit(self):
        #获取用户数据的卡号
        cardid=int(input('Please enter your card number: '))
        #验证卡号是否存在
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #获取卡对象
        cardobj=self.cardid_userobj_dict[cardid].card
        #如果存在，则验证密码
        if self.__checkpwd(cardobj):
            #验证是否锁卡
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
                #获取存款金额
                deposit=int(input('Please enter your deposit amount: '))
                #存款金额不能小于0
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

    #4.取款功能
    def withdrawal(self):
        #获取用户卡号
        cardid=int(input('Please enter your card number: '))
        #验证输入的卡号是否存在
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #获取卡对象
        cardobj=self.cardid_userobj_dict[cardid].card
        #如果卡存在，则验证密码
        if self.__checkpwd(cardobj):
            #验证是否锁卡
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
                #获取取款金额
                withdrawal=int(input('Please enter your withdrawal amount: '))
                #取款金额不能大于卡上现有余额
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

    #5.转账功能
    def transfer(self):
        #获取用户转出的卡号
        cardid=int(input('Please enter your card number: '))
        #验证输入的转出卡号是否存在
        if cardid not in self.cardid_userobj_dict:
            print('''
********************************************
*                                          *
* This entered card number does not exist. *
*                                          *
********************************************
''')
            return
        #获取收款卡号和收款方姓名
        cardid_recipient=int(input('Please enter the card number of the recipient: '))
        name_recipient=input('Please enter the name of the recipient: ')
        #获取卡对象
        cardobj=self.cardid_userobj_dict[cardid].card
        #如果卡存在，则验证密码
        if self.__checkpwd(cardobj):
            #验证是否锁卡
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
                #获取转账金额
                transfer=int(input('Please enter your transfer amount: '))
                #转出金额不能大于卡上现有余额
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

    #6.修改密码
    def change_password(self):
        #获取用户卡号
        cardid=int(input('Please enter your card number: '))
        #验证用户卡号是否存在
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
            #让用户选择使用 身份证 或者 原密码 进行密码修改
            num_pwd=input('''
***************************************
*                                     *
*  (1) Original password (2) User ID  *
*                                     *
***************************************

Please select the mode to change your password:
''')
            #验证用户输入的数字是否正确
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
                #选择使用【原密码】进行密码修改
                #获取卡对象
                cardobj=self.cardid_userobj_dict[cardid].card
                #先验证原密码
                if self.__checkpwd(cardobj):
                    #验证是否锁卡
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
                        #设定新密码
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
                        #跳出本次循环
                        return
            if num_pwd=='2':
                #选择使用【身份证】进行密码修改
                #获取用户对象
                userobj=self.cardid_userobj_dict[cardid]
                cardobj=userobj.card
                #先验证身份证号码
                if self.__checkuserid(userobj):
                    #获取卡对象
                    cardobj=userobj.card
                    #验证是否锁卡
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
                        #设定新密码
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
    #7.锁卡功能
    def lockcard(self):
        print('Lock card ')
    #8.解卡功能
    def unlockcard(self):
        print('Unlock card ')
    #9.补卡功能
    def replacecard(self):
        print('Replace card ')
    #0.退出
    def exit(self):
        #把当前数据，写入到文件中
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

    #获取用户名的私有方法
    def __getusername(self):
        while True:
            name=input('Please enter your name: ')
            if not name:
                print('The name you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return name
    #获取用户身份证号的私有方法
    def __getuserid(self):
        while True:
            userid=int(input('Please enter your ID: '))
            if not userid:
                print('The ID you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return userid
    #获取用户电话号码的私有方法
    def __getphone_num(self):
        while True:
            phone_num=int(input('Please enter your phone number: '))
            if not phone_num:
                print('The phone number you have entered is incorrect, please re-enter it: ')
                continue
            else:
                return phone_num
    #获取用户密码的私有方法
    def __getpwd(self):
        while True:
            pwd=int(input('Please enter your password: '))
            if not pwd:
                print('The password you have entered is incorrect, please re-enter it: ')
                continue
            else:
                #密码输入正确后，再次输入确认密码
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

    #获取用户设置的新密码的方式
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
                #密码输入正确后，再次输入确认密码
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

    #检测密码是否正确
    def __checkpwd(self,cardobj):
        num=3
        while True:
            #获取密码
            pwd=int(input('Please enter your password: '))
            #检测密码是否正确
            if pwd==cardobj.pwd:
                return True
            else:
                num=num-1
                if num==0:
                    #直接锁卡
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

    #检验身份证是否正确
    def __checkuserid(self,userobj):
        while True:
            #获取身份证号码
            userid=int(input('Please enter your user ID number: '))
            #检验身份证号码是否正确
            if userid==userobj.userid:
                return True
            else:
                #锁卡
                self.userobj.card.islock=True
                print('''
***************************************
*                                     *
* Wrong user ID, your card is locked. *
*                                     *
***************************************
''')
                break
