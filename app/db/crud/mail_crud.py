from O365.utils.token import BaseTokenBackend, log
from sqlalchemy.exc import SQLAlchemyError

from app.db.base import SessionLocal
from app.models.table_model import Token as TokenModel


class PostgresBackend(BaseTokenBackend):
    def __init__(self):
        super().__init__()

    def load_token(self):
        """
        Retrieves the token from the database
        :return dict or None: The token if exists, None otherwise
        """
        token = None
        db = SessionLocal()
        try:
            token_model = db.query(TokenModel).filter_by(type='Microsoft').first()
            if token_model:
                token = token_model.content
            db.close()
        except SQLAlchemyError as e:
            log.error("Token could not be retrieved from the backend: {}".format(e))

        return token

    def save_token(self) -> bool:
        """
        Saves the token dict in the database
        :return bool: Success / Failure
        """
        if self.token is None:
            raise ValueError('You have to set the "token" first.')
        db = SessionLocal()
        try:
            token_model = TokenModel(
                type='Microsoft',
                content=self.token
            )
            db.add(token_model)
            db.commit()
            return True
        except SQLAlchemyError as e:
            log.error("Token could not be saved: {}".format(e))
            return False
        finally:
            db.close()

    def delete_token(self) -> bool:
        """
        Deletes the token from the database
        :return bool: Success / Failure
        """
        db = SessionLocal()
        try:
            token_model = db.query(TokenModel).filter_by(type='Microsoft').first()
            if token_model:
                db.delete(token_model)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            log.error("Token could not be deleted from the backend: {}".format(e))
            # 在这里处理数据库错误，根据需要进行日志记录或其他操作
            return False
        finally:
            db.close()

    def check_token(self) -> bool:
        """
        Checks if the token exists in the database
        :return bool: True if exists, False otherwise
        """
        db = SessionLocal()
        try:
            token_model = db.query(TokenModel).filter_by(type='Microsoft').first()
            return token_model is not None
        except SQLAlchemyError as e:
            log.error("Error checking token existence: {}".format(e))
            # 在这里处理数据库错误，根据需要进行日志记录或其他操作
            return False
        finally:
            db.close()
