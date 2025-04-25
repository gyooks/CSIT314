from db_config import db
from entity.UserAccount import User, UserProfile
from sqlalchemy import or_

class SearchUserController:
    def search_user(self, keyword):
        return db.session.query(User, UserProfile).outerjoin(
            UserProfile, User.userID == UserProfile.user_id
        ).filter(
            or_(
                User.email.ilike(f'%{keyword}%'),
                User.phone.ilike(f'%{keyword}%'),
                UserProfile.first_name.ilike(f'%{keyword}%'),
                UserProfile.last_name.ilike(f'%{keyword}%')
            )
        ).all()