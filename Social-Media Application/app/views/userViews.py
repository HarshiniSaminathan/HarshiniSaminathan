from flask import Blueprint

from app.service.userService import (user_Sign_Up, login, addProfile, token_required, unFollowFriend, veiw_Profile,
                                     following_List, Followers_List, view_Post, post_Comments, update_Read_Status,
                                     log_Out, add_post, deletePost, requestForFollow, block_Friend, unblock_Friend,
                                     block_list, filter_By_username, like_The_Post, Reply_For_Comments,
                                     search_Username, unlike_The_Post, responding_For_followRequest,
                                     view_Friends_Profile, view_Post_Of_ParticularFriend, delete_Comments,
                                     post_Messages, delete_Message, get_Messages_BY_Emailid, get_Post_By_Hashtags)

userapi_blueprint = Blueprint('userapi', __name__, url_prefix='/api/user')


@userapi_blueprint.route("signUp",methods=['POST'])
def userSignUp():
    return user_Sign_Up()

@userapi_blueprint.route("login",methods=['GET'])
def user_login():
    return login()

@userapi_blueprint.route("AddProfile",methods=['POST'])
@token_required(['USER'])
def add_Profile():
    return addProfile()

@userapi_blueprint.route("logout",methods=['GET'])
@token_required(['USER'])
def logout():
    return log_Out()

@userapi_blueprint.route("addPost",methods=['POST'])
@token_required(['USER'])
def addPost():
    return add_post()

@userapi_blueprint.route("deletePost",methods=['DELETE'])
@token_required(['USER'])
def delete_Post():
    return deletePost()

@userapi_blueprint.route("requestForFollow",methods=['POST'])
@token_required(['USER'])
def requesting_for_follow():
    return requestForFollow()

@userapi_blueprint.route("respondingForfollowRequest",methods=['PUT'])
@token_required(['USER'])
def respondingForfollowRequest():
    return responding_For_followRequest()

@userapi_blueprint.route("unfollow",methods=['DELETE'])
@token_required(['USER'])
def unFollow():
    return unFollowFriend()

@userapi_blueprint.route("veiwProfile",methods=['GET'])
@token_required(['USER'])
def veiwProfile():
    return veiw_Profile()

@userapi_blueprint.route("followingList",methods=['GET'])
@token_required(['USER'])
def followingList():
    return following_List()  # users who I follow

@userapi_blueprint.route("FollowersList",methods=['GET'])
@token_required(['USER'])
def FollowersList():
    return Followers_List()  # users who follow me

@userapi_blueprint.route("viewFriendsProfile",methods=['GET'])
@token_required(['USER'])
def viewFriendsProfile():
    return view_Friends_Profile()

@userapi_blueprint.route("viewPostOfAllFollowingUsers",methods=['GET'])
@token_required(['USER'])
def viewPost():
    return view_Post()

@userapi_blueprint.route("viewPostOfParticularFriend",methods=['GET'])
@token_required(['USER'])
def viewPostOfParticularFriend():
    return view_Post_Of_ParticularFriend()

@userapi_blueprint.route("blockFriend",methods=['PUT'])
@token_required(['USER'])
def blockFriend():
    return block_Friend()

@userapi_blueprint.route("unblockFriend",methods=['PUT'])
@token_required(['USER'])
def unblockFriend():
    return unblock_Friend()

@userapi_blueprint.route("blockList",methods=['GET'])
@token_required(['USER'])
def blockList():
    return block_list()

@userapi_blueprint.route("filterByusername",methods=['GET'])
@token_required(['USER'])
def filterByusername():
    return filter_By_username()
@userapi_blueprint.route("likeThePost",methods=['POST'])
@token_required(['USER'])
def likeThePost():
    return like_The_Post()

@userapi_blueprint.route("unlikeThePost",methods=['DELETE'])
@token_required(['USER'])
def unlikeThePost():
    return unlike_The_Post()

@userapi_blueprint.route("searchUsername",methods=['GET'])
@token_required(['USER'])
def searchUsername():
    return search_Username()

@userapi_blueprint.route("postComments",methods=['POST'])
@token_required(['USER'])
def postComments():
    return post_Comments()

@userapi_blueprint.route("ReplyForComments",methods=['PUT'])
@token_required(['USER'])
def ReplyForComments():
    return Reply_For_Comments()

@userapi_blueprint.route("deleteComments",methods=['DELETE'])
@token_required(['USER'])
def deleteComments():
    return delete_Comments()

@userapi_blueprint.route("postMessages",methods=['POST'])
@token_required(['USER'])
def postMessages():
    return post_Messages()

@userapi_blueprint.route("deleteMessage",methods=['DELETE'])
@token_required(['USER'])
def deleteMessage():
    return delete_Message()

@userapi_blueprint.route("getMessagesBYEmailid",methods=['GET'])
@token_required(['USER'])
def getMessagesBYEmailid():
    return get_Messages_BY_Emailid()

@userapi_blueprint.route("updateReadStatus",methods=['PUT'])
@token_required(['USER'])
def updateReadStatus():
    return update_Read_Status()

@userapi_blueprint.route("getPostByHashtags",methods=['GET'])
@token_required(['USER'])
def getPostByHashtags():
    return get_Post_By_Hashtags()
