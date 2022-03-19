class Card():
    #Card number, PIN, balance and whether the card is locked
    def __init__(self,cardid,pwd,balance,islock=False):
        self.cardid=cardid  #card number
        self.pwd=pwd  #PIN
        self.balance=balance  #balance
        self.islock=islock #'false' is unlocked，'true' is locked.
