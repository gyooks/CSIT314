from db_config import db
from entity.UserAccount import User, UserProfile

class SearchUserController:
    def search_user(self, keyword):
        return db.session.query(User, UserProfile).join(UserProfile, User.userID == UserProfile.user_id).filter(
            (User.email.ilike(f'%{keyword}%')) |
            (User.phone.ilike(f'%{keyword}%')) |
            (UserProfile.first_name.ilike(f'%{keyword}%')) |
            (UserProfile.last_name.ilike(f'%{keyword}%'))
        ).all()
