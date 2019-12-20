import Dcard
if __name__ == "__main__":
    user = Dcard.Dcard()
    user.getForumsInfor('nkfust', popular=True, limit=30)
    #user.downloadImage()
    user.getThisInfo()
