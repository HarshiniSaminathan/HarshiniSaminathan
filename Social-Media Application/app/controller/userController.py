import datetime

from app.models.postsModel import Post
from app.models.userModel import User
from app.models.followersModel import Followers
from app.models.userProfileModel import UserProfile
from app.models.likeModel import Like
from app.models.commentsModel import Comments
from datetime import datetime, timedelta



def check_email_existence(emailid):
    return User.objects(emailid=emailid).first() is not None

def check_postid(postid):
    return Post.objects(id=postid).first() is not None


def check_username_existence(username):
    return User.objects(username=username,status='ACTIVE').first() is not None

def check_email_For_Username(emailid):
    return User.objects(emailid=emailid,status='ACTIVE').first() is not None

def insert_user(emailid, password, username, fullname, role, status,accountType):
    current_time = datetime.utcnow()
    user = User(
        emailid=emailid,
        password=password,
        username=username,
        fullname=fullname,
        role=role,
        status=status,
        accountType=accountType,
        created_at=current_time
    )
    user.save()

def check_login(emailid, password):
    try:
        user = User.objects(emailid=emailid, password=password).first()
        return user
    except Exception as e:
        print(f"Error in check_login: {e}")
        return None

def add_profile(emailid,filename,profileName,Bio):
    userprofile = UserProfile(emailid=emailid,profileImage=filename,profileName=profileName,bio=Bio)
    userprofile.save()


def updateSessionCode(emailid, session_code):
    try:
        user = User.objects(emailid=emailid).first()
        if user:
            user.sessionCode = session_code
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in updateSessionCode: {e}")
        return False

def check_emailhas_sessionCode(email,session_code):
    return User.objects(emailid=email,sessionCode=session_code).first() is not None

def deleteSession(email):
    try:
        user = User.objects(emailid=email).first()

        if user:
            user.sessionCode = None
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in deleteSession: {e}")
        return False

def addPost(emailid,postType,filename,caption,tagUsername,status):
    created_at = datetime.utcnow()
    user= Post(emailid=emailid,postType=postType,post=str(filename),caption=caption,tagUsername=tagUsername,created_at=created_at,status=status)
    user.save()


def delete_Post(emailid, created_at):
    try:
        post=Post.objects(emailid=emailid,created_at=created_at)
        if post:
            post.delete()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in deletePost: {e}")
        return False


def check_post_exists(emailid,created_at):
    return Post.objects(emailid=emailid,created_at=created_at).first() is not None


def status_for_request(emailid,followerEmailid):
    try:
        follower = Followers.objects(emailid=emailid, followerEmailid=followerEmailid).first()
        return follower
    except Exception as e:
        print(f"Error in check_login: {e}")
        return None


def request_to_follow(emailid,followerEmailid,status):
    created_at = datetime.utcnow()

    Follower = Followers(emailid=emailid, followerEmailid=followerEmailid,
                request_at=created_at,status=status)
    Follower.save()


def responding_For_Resquest(emailid, followerEmailid,statusToDone):
    try:
        user=Followers.objects(emailid=emailid,followerEmailid=followerEmailid).first()
        if user:
            created_at = datetime.utcnow()
            user.status=statusToDone
            user.request_at=created_at
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in updateSessionCode: {e}")
        return False

def unfollow_friend(emailid,followerEmailid):
    try:
        follower = Followers.objects(emailid=emailid,followerEmailid=followerEmailid)
        if follower:
            follower.delete()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in deletePost: {e}")
        return False


def Get_Profile_Info(emailid,page, per_page):

    required_fields = {'emailid': None, 'profileImage': None, 'profileName': None, 'bio': None}

    following_email = Followers.objects(emailid=emailid).first()
    total_following = User.objects(emailid=following_email.followerEmailid).count() if following_email else 0

    follower_email = Followers.objects(followerEmailid=emailid).first()
    total_followers = User.objects(emailid=follower_email.emailid).count() if follower_email else 0

    total_posts = Post.objects(emailid=emailid).count()

    get_profile = UserProfile.objects(emailid=emailid).only(*required_fields.keys()).paginate(page=page, per_page=per_page)
    if get_profile:

        total_pages = (get_profile.total / per_page) + (get_profile.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in get_profile.items],total_following,total_followers,total_posts, int(total_pages)
    return None,int(0),int(0),int(0),int(0)




def List_following(emailid,page, per_page):
    required_fields = {'username':None}

    get_following_email = Followers.objects(emailid=emailid).first()
    if get_following_email:
        print(get_following_email.followerEmailid)
        get_List_username = User.objects(emailid=get_following_email.followerEmailid).only(*required_fields.keys()).paginate(page=page, per_page=per_page)

        total_pages = (get_List_username.total / per_page) + (get_List_username.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in get_List_username.items], int(total_pages),get_List_username.total
    return None, int(0), int(0)

def List_followers(emailid,page, per_page):
    required_fields = {'username':None}

    get_follower_email = Followers.objects(followerEmailid=emailid).first()
    if get_follower_email:
        print(get_follower_email.emailid)
        get_List_username = User.objects(emailid=get_follower_email.emailid).only(*required_fields.keys()).paginate(page=page, per_page=per_page)

        total_pages = (get_List_username.total / per_page) + (get_List_username.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in get_List_username.items], int(total_pages),get_List_username.total
    return None,int(0),int(0)




def Get_friends_profile(followerEmailid, page, per_page):

    required_fields = {'emailid': None, 'profileImage': None, 'profileName': None, 'bio': None}

    following_email = Followers.objects(emailid=followerEmailid).first()
    total_following = User.objects(emailid=following_email.followerEmailid).count() if following_email else 0

    follower_email = Followers.objects(followerEmailid=followerEmailid).first()
    total_followers = User.objects(emailid=follower_email.emailid).count() if follower_email else 0

    total_posts = Post.objects(emailid=followerEmailid).count()

    get_profile = UserProfile.objects(emailid=followerEmailid).only(*required_fields.keys()).paginate(page=page, per_page=per_page)
    if get_profile:

        total_pages = (get_profile.total / per_page) + (get_profile.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in get_profile.items],total_following,total_followers,total_posts, int(total_pages)
    return None,int(0),int(0),int(0),int(0)



def Get_friends_post(emailid, page, per_page):

    required_fields = {'id': None, 'emailid': None, 'postType': None, 'post': None, 'caption': None, 'created_at': None,
                       'tagUsername': None}
    get_following_email = Followers.objects(emailid=emailid, status='ACCEPTED').first()

    if get_following_email:
        get_List_Post = Post.objects(emailid=get_following_email.followerEmailid, status='ACTIVE').only(
            *required_fields.keys()).paginate(page=page, per_page=per_page)

        if get_List_Post:
            total_pages = (get_List_Post.total / per_page) + (get_List_Post.total % per_page > 0)
            profile = []

            for post in get_List_Post.items:
                post_info = {field: getattr(post, field) for field in required_fields}

                likes = Like.objects(postid=str(post.id))
                count=Like.objects(postid=str(post.id)).count()

                post_info['likes'] = [
                    {
                        'emailid': like.emailid,
                        'created_at': like.created_at,

                    }
                    for like in likes
                ]

                comments = Comments.objects(postid=str(post.id))
                comment_count=Comments.objects(postid=str(post.id)).count()
                post_info['comments'] = [
                    {
                        'id': str(comment.id),
                        'emailid': comment.emailid,
                        'comment': comment.comments,
                        'created_at': comment.created_at,

                    }
                    for comment in comments
                ]
                profile.append(post_info)
                profile.append({"Like-count": count, "Comment-Count": comment_count})
            return profile, int(total_pages)

    return None, int(0)

def Get_Particular_friends_post(emailid, page, per_page):
    required_fields = {'emailid': None, 'postType': None, 'post': None, 'caption': None, 'created_at': None,
                       'tagUsername': None}
    get_List_Post = Post.objects(emailid=emailid, status='ACTIVE').only(*required_fields.keys()).paginate(page=page,
                                                                                                          per_page=per_page)
    if get_List_Post:
        total_pages = (get_List_Post.total / per_page) + (get_List_Post.total % per_page > 0)

        result = []
        for post in get_List_Post.items:
            like_count = Like.objects(id=post.id).count()

            post_info = {field: getattr(post, field) for field in required_fields}
            post_info['like_count'] = like_count

            result.append(post_info)

        return result, int(total_pages), get_List_Post.total
    return None, int(0),int(0)


def check_account_Type(followerEmailid):
    return User.objects(emailid=followerEmailid,accountType='PUBLIC').first() is not None


def activatePost(postid,status):
    try:

        user=Post.objects(id=postid).first()
        print(user.status)
        if user.status == 'INACTIVE':
            user.status=status
            print(user.status)
            user.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Status: {e}")
        return False


def block_friend(emailid,followingEmailid):
    try:
        block=Followers.objects(emailid=emailid,followerEmailid=followingEmailid).first()
        if block:
            block.status='BLOCK'
            block.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Status: {e}")
        return False


def unblock_friend(emailid,followingEmailid):
    try:
        block=Followers.objects(emailid=emailid,followerEmailid=followingEmailid).first()
        if block:
            block.status='UNBLOCK'
            block.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Status: {e}")
        return False

def Get_block_list(emailid,page,per_page):
    required_fields = {'username': None}
    get_follower_email = Followers.objects(emailid=emailid,status='BLOCK').first()
    if get_follower_email:
        print(get_follower_email.followerEmailid)
        get_List_username = User.objects(emailid=get_follower_email.followerEmailid).only(*required_fields.keys()).paginate(
            page=page, per_page=per_page)

        total_pages = (get_List_username.total / per_page) + (get_List_username.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in get_List_username.items], int(
            total_pages), get_List_username.total
    return None, int(0), int(0)

def likepost(postid,emailid):
    created_at = datetime.utcnow()
    print(postid)
    try:
        if postid:
            Likes = Like(postid=str(postid),emailid=emailid,created_at=created_at)
            Likes.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Liking: {e}")
        return False


def unlikepost(postid,emailid):
    try:
        if postid:
            Likes = Like.objects(postid=str(postid),emailid=emailid).first()
            Likes.delete()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Liking: {e}")
        return False

from math import ceil
from mongoengine import Q
def search_username(Username,page,per_page):
    required_fields = {'username': None}
    user_filter = Q(username__icontains=Username)
    users = User.objects(user_filter).only(*required_fields.keys()).paginate(page=page, per_page=per_page)

    if not users:
        return None, 0

    res = [{field: getattr(profile, field) for field in required_fields} for profile in users.items]
    total_pages = ceil(users.total / per_page)

    for i in res:
        username = i['username']
        print(username)
        required_fields = {'emailid': None, 'profileImage': None, 'profileName': None, 'bio': None}

        emailId_By_username = User.objects(username=username).first()
        emailid = emailId_By_username.emailid

        following_email = Followers.objects(emailid=emailid).first()
        total_following = User.objects(emailid=following_email.followerEmailid).count() if following_email else 0

        follower_email = Followers.objects(followerEmailid=emailid).first()
        total_followers = User.objects(emailid=follower_email.emailid).count() if follower_email else 0

        total_posts = Post.objects(emailid=emailid).count()

        get_profile = UserProfile.objects(emailid=emailid).only(*required_fields.keys()).paginate(page=page,
                                                                                                  per_page=per_page)

        if get_profile:
            return [{field: getattr(user, field) for field in required_fields} for user in
                    get_profile.items], total_following, total_followers, total_posts, int(total_pages), username

        return None, int(0), int(0), int(0), int(0), None

def Get_Profile_Info_ByUsername(username,page,per_page):
    required_fields = {'emailid': None, 'profileImage': None, 'profileName': None, 'bio': None}

    emailId_By_username = User.objects(username=username).first()
    emailid = emailId_By_username.emailid

    following_email = Followers.objects(emailid=emailid).first()
    total_following = User.objects(emailid=following_email.followerEmailid).count() if following_email else 0

    follower_email = Followers.objects(followerEmailid=emailid).first()
    total_followers = User.objects(emailid=follower_email.emailid).count() if follower_email else 0

    total_posts = Post.objects(emailid=emailid).count()

    get_profile = UserProfile.objects(emailid=emailid).only(*required_fields.keys()).paginate(page=page,
                                                                                              per_page=per_page)
    if get_profile:
        total_pages = (get_profile.total / per_page) + (get_profile.total % per_page > 0)

        return [{field: getattr(user, field) for field in required_fields} for user in
                get_profile.items], total_following, total_followers, total_posts, int(total_pages)
    return None, int(0), int(0), int(0), int(0)

def save_comments(postid,comments,emailid):
    created_at = datetime.utcnow()
    try:
        Comment = Comments(emailid=emailid, postid=postid,
                             comments=comments, created_at=created_at)
        Comment.save()
        return True
    except Exception as e:
        print(f"Error in Status: {e}")
        return False
def save_replycomments(commentid,replycomments,emailid):
    try:
        comment = Comments.objects(id=commentid).first()
        if comment:
            created_at = datetime.utcnow()
            reply_data = {"emailid": emailid, "replycomment": replycomments,"created_at":created_at}
            comment.replyComment.append(reply_data)
            comment.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in reply comments: {e}")
        return False

def deletecomment(emailid,commentid):
    try:
        comment=Comments.objects(emailid=emailid,id=commentid).first()
        if comment:
            comment.delete()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in reply comments: {e}")
        return False


