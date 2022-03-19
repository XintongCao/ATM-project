class Card():
    #卡号，密码，余额，是否锁卡
    def __init__(self,cardid,pwd,balance,islock=False):
        self.cardid=cardid  #卡号
        self.pwd=pwd  #密码
        self.balance=balance  #余额
        self.islock=islock #false是未锁卡，true为锁卡状态
