from fastapi import FastAPI, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schema
from settings import get_db, logger
from model import Users
from src.utils import get_hashed_password, create_access_token, verify_password

app = FastAPI()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

# let's create router
router = APIRouter(
    prefix='/login',
    tags=['addition']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def SignUp(payload: schema.UserSignup, db: Session = Depends(get_db)):
    try:
        query = db.query(Users).filter(Users.email == payload.email)
        print(payload.email)
        print('data')
        if not query[0].email:
            user_data = {
                'email': payload.email,
                'password': get_hashed_password(payload.password)
            }
            new_note = Users(**user_data)
            db.add(new_note)
            db.commit()
            db.refresh(new_note)
            data = {
                'response_code': 200,
                'Status': 'Success',
                'data': []
            }
            logger.info("Signup process finished")
            return data
        else:
            data = {
                'response_code': 400,
                'Status': 'Failed',
                'data': []
            }
            logger.error("Signup process failed")
            return data
    except Exception as e:
        data = {
            'response_code': 500,
            'Status': 'Failed',
            'data': str(e)
        }
        logger.error("Signup process failed")
        return data


@router.post('/login')
def Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        query = db.query(Users).filter(Users.email == form_data.username).all()
        if not query[0].email:
            data = {
                'response_code': 400,
                'Status': 'Failed',
                'data': 'Email does not exists!!'
            }
            return data
        hashed_pass = query[0].password
        if not verify_password(form_data.password, hashed_pass):
            data = {
                'response_code': 400,
                'Status': 'Failed',
                'data': 'Email (or) Password wrong!!'
            }
            return data
        access_token = create_access_token(query[0].email)
        # refresh_token = create_refresh_token(query[0].email)
        data = {
            'response_code': 200,
            'Status': 'Success',
            'data': {
                'access_token': access_token,
                # 'refresh_token': refresh_token,
            }
        }
        print(data)
        return data
    except Exception as e:
        data = {
            'response_code': 500,
            'Status': 'Failed or Internal server error',
            'data': str(e)
        }
        return data


@router.put('/update_password')
def Update_password(payload: schema.UpdatePassword, db: Session = Depends(get_db),
                    token: str = Depends(reuseable_oauth)):
    try:
        query = db.query(Users).filter(Users.email == payload.email)
        if not query[0].email:
            data = {
                'response_code': 400,
                'Status': 'Not a valid user',
                'data': []
            }
            return data
        hashed_password = query[0].password
        if not verify_password(payload.old_password, hashed_password):
            data = {
                'response_code': 400,
                'Status': 'Old password not matching!!',
                'data': []
            }
            return data
        update_pass = get_hashed_password(payload.new_password)
        query.update({'password': update_pass})
        # query[0].password =
        db.commit()
        # db.refresh(update_pass)
        data = {
            'response_code': 200,
            'Status': 'Success',
            'data': 'password changed successfully!!'
        }
        return data
    except Exception as e:
        data = {
            'response_code': 500,
            'Status': 'Failed',
            'data': f'Internal Server Error, str({e})'
        }
        return data


@router.post('/forgot_password')
def Forgot_password(payload: schema.ForgotPassword, db: Session = Depends(get_db)):
    try:
        query = db.query(Users).filter(Users.email == payload.email)
        if not query:
            data = {
                'response_code': 400,
                'Status': "You're not a user!!",
                'data': []
            }
            return data
        otp_value = 5678
        query.update({'phone_number': otp_value})
        db.commit()
        data = {
            'response_code': 200,
            'Status': 'Success',
            'data': 'OTP sent successfully!!'
        }
        return data
    except Exception as e:
        data = {
            'response_code': 500,
            'Status': 'Failed',
            'data': f'Internal Server Error, str({e})'
        }
        return data


@router.post('/reset_password')
def Reset_password(payload: schema.ResetPassword, db: Session = Depends(get_db)):
    try:
        query = db.query(Users).filter(Users.email == payload.email)
        if not query:
            data = {
                'response_code': 400,
                'Status': "You're not a user!!",
                'data': []
            }
            return data
        if not query[0].phone_number == payload.otp:
            data = {
                'response_code': 400,
                'Status': "OTP not matching!!, Please give the valid OTP",
                'data': []
            }
            return data
        new_pass = get_hashed_password(payload.password)
        query.update({'password': new_pass})
        db.commit()
        data = {
            'response_code': 200,
            'Status': 'Success',
            'data': 'password updated successfully!!'
        }
        return data
    except Exception as e:
        data = {
            'response_code': 500,
            'Status': 'Failed',
            'data': f'Internal Server Error, str({e})'
        }
        return data
