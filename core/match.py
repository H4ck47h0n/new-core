null = None
from core.models import User
max_id =len( User.query.all())
def die(arg):
    print('Runtime error:' + arg)
    raise Exception


def calcAttrSimilarity(attr1, attr2, weight):
    if attr1 == '' or attr2 == '':  return 0
    if len(attr1) != len(attr2):
        die('len attr1 and len attr2 mismatch.')
    if len(attr1) != len(weight):
        die('len attr and len weight mismatch.')
    nsame = 0
    for i in range(len(attr1)):
        char1 = attr1[i]
        char2 = attr2[i]
        nsame += (char1 == char2) * weight[i]
    return int(nsame)


def getUnSeenUsers(like, dislike):
    matrix = [1] * (max_id+1)
    for string in (like, dislike):
        if len(string) % 2 != 0:
            die('len of like and dislike should be even but got odd')
        for i in range(int(len(string) / 2)):
            uid = int(string[2 * i:2 * i + 2])
            matrix[uid] = 0
    UnseenUsers = []
    for i in range(1,max_id+1):
        if matrix[i]:
            UnseenUsers.append(i)
    return UnseenUsers


def getUserAttr(User, uid):
    if uid > max_id: return
    user = User.query.filter_by(id=uid).all()[0]
    if user == null:
        die('expect user got null.')
    return user.exiting


def getUserLikeDislike(User, uid):
    user = User.query.filter_by(id=uid).all()[0]
    if user == null:
        die('expect user got null.')
    return (user.likes, user.dislikes)


def getMatchedUser(User, uid):
    weight = (20, 20, 20, 20, 20)
    attrUser = getUserAttr(User, uid)
    likeDislike = getUserLikeDislike(User, uid)
    UnseenUsers = getUnSeenUsers(likeDislike[0], likeDislike[1])
    # print(UnseenUsers)
    for i in range(len(UnseenUsers)):
        UnseenUsers[i] = (UnseenUsers[i], calcAttrSimilarity(
            attrUser, getUserAttr(User, UnseenUsers[i]), weight))
        print(UnseenUsers[i])
    UnseenUsers = tuple(sorted(UnseenUsers, key=lambda x: x[1]))
    return(UnseenUsers[-1])


# def test1():
# 	a = "10101010100"
# 	b = "10101010111"
# 	weight = (10,10,10,10,10,10,10,10,10,10)
# 	print(calcAttrSimilarity(a,b,weight))

# def test2():
# 	a = [('xiaoming',20),('zhangsan',40),('nidie',10)]
# 	print(tuple(sorted(a,key=lambda x : x[1]))[-1])

# def test3():
# 	like = '000204060899'
# 	dislike = '010798'
# 	print(getUnSeenUsers(like,dislike))

# test2()
