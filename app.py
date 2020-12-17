import base64
import linecache
import random
from datetime import datetime, timedelta
from io import BytesIO

from PIL import Image
from captcha.image import ImageCaptcha
from flask import Flask, render_template, request
from flask_cors import CORS

import captcha_sets
import config
import const
import oauth
import security
from models import User, AccessToken, Answer, Captcha

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/ru')
@app.route('/en')
def index():
    return render_template('index.html', lang=detect_lang(), site_host=config.site_host)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/facebook/delete')
def delete_facebook_data():
    return render_template('deletion.html')


@app.route('/auth/<provider>')
def auth(provider):
    if provider not in ['facebook', 'vk', 'google']:
        return f"Unknown auth provider: {provider}", 403

    if security.user() is not None:
        return render_template('auth_failed.html', err="Already authorized", provider=provider,
                               lang=security.user().lang), 403

    code = request.args.get('code', None)

    try:
        if provider == 'vk':
            user_id, token = oauth.vk_token(code)
        elif provider == 'facebook':
            user_id, token = oauth.fb_token(code)
        elif provider == 'google':
            user_id, token = oauth.google_token(code)
        else:
            raise RuntimeError('Unknown provider')
    except RuntimeError:
        return render_template('auth_failed.html', err="Cannot get token", provider=provider,
                               lang=detect_lang()), 400

    user = User.get_or_none(User.source == provider, User.source_id == user_id)
    if not user:
        try:
            name = oauth.get_user_name(provider, user_id, token)
            user = User.create(source=provider, source_id=user_id, lang=detect_lang(), name=name)
        except:
            user = None

    if not user:
        return render_template('auth_failed.html', err="Cannot create user", provider=provider, lang=detect_lang()), 500

    token = AccessToken.create(user, expire_in_days=7)
    return render_template('auth_success.html', token=token.token, user=user)


@app.route('/user', methods=['GET'])
@security.protected
def user_info():
    user = security.user()
    if not user:
        return {}, 401
    user_answer = user.get_answer()

    return {
        "name": user.name,
        "lang": user.lang,
        "step": None if user_answer is None else user_answer.step
    }


@app.route('/user', methods=['PATCH'])
@security.protected
def update_lang():
    user = security.user()
    if not user:
        return {}, 401

    lang = request.json.get('lang')
    if lang not in ['ru', 'en']:
        return {}, 400

    user.lang = lang
    user.save()

    return {}


@app.route('/stats', methods=['GET'])
@security.protected
def stats():
    user = security.user()
    if not user:
        return {}, 401
    user_answer = user.get_answer()
    if user_answer is None or user_answer.step != const.STEP_CAPTCHA_SOLVED:
        return {}, 403

    humans = Answer.select().where(Answer.step == const.STEP_CAPTCHA_SOLVED, Answer.value == 0).count()
    robots = Answer.select().where(Answer.step == const.STEP_CAPTCHA_SOLVED, Answer.value == 1).count()

    return {"answer": user_answer.value, "humans": humans, "robots": robots}


@app.route('/captcha', methods=['GET'])
@security.protected
def captcha():
    user = security.user()
    if not user:
        return {}, 401
    user_answer = user.get_answer()
    if user_answer is None or user_answer.step == const.STEP_CAPTCHA_SOLVED:
        return {}, 403

    step = user_answer.step
    code = Captcha.generate_code()
    random.seed(code)

    if step == 0:
        answer = random.randint(1000, 9999)
        Captcha.create(code=code, value=answer, expire_at=datetime.utcnow() + timedelta(minutes=5))

        return {
            'code': code,
            'question': answer
        }
    elif step == 1:
        answer = linecache.getline('captcha/words.txt', random.randint(0, 825)).strip()
        image_captcha = ImageCaptcha(fonts=['captcha/font.ttf'], width=320, height=120)
        image = image_captcha.generate(answer)
        Captcha.create(code=code, value=answer, expire_at=datetime.utcnow() + timedelta(minutes=5))

        return {
            'code': code,
            'image': base64.b64encode(image.read()).decode('utf-8')
        }
    elif step == 2:
        group = random.randint(0, 5)
        answers_length = random.randint(3, 5)

        answers = []
        while len(answers) < answers_length:
            while True:
                ans = random.choice(captcha_sets.GROUPS[group])
                if ans not in answers:
                    break
            answers.append(ans)

        rest_images = [x for x in captcha_sets.ALL if x not in captcha_sets.GROUPS[group]]
        images = [
            *answers,
        ]
        while len(images) < 9:
            while True:
                img = random.choice(rest_images)
                if img not in images:
                    break
            images.append(img)
        random.shuffle(images)

        answer = "".join([str(i) for i in range(0, 9) if images[i] in captcha_sets.GROUPS[group]])
        Captcha.create(code=code, value=answer, question=group, expire_at=datetime.utcnow() + timedelta(minutes=5))

        images_b64 = []
        for image in images:
            img = Image.open(f'captcha/sets/{image}')
            img.thumbnail((64, 64))

            out = BytesIO()
            img.save(out, "JPEG", quality=85)
            out.seek(0)

            images_b64.append(base64.b64encode(out.read()).decode('utf-8'))

        return {
            'code': code,
            'images': images_b64,
            'question': captcha_sets.NAMES[group]
        }


@app.route('/captcha', methods=['POST'])
@security.protected
def check_captcha():
    user = security.user()
    if not user:
        return {}, 401

    user_answer = user.get_answer()
    if user_answer is None or user_answer.step == const.STEP_CAPTCHA_SOLVED:
        return {}, 403

    code = request.json.get('code')
    answer = request.json.get('answer')

    captcha = Captcha.get_or_none(Captcha.code == code)
    if captcha.expire_at <= datetime.utcnow():
        return {'error': 'Captcha expired'}, 400

    if captcha.value != answer:
        return {'error': 'Invalid captcha'}, 400

    captcha.expire_at = datetime.utcnow()
    captcha.save()

    user_answer.step += 1
    user_answer.save()

    if user_answer.step != const.STEP_CAPTCHA_SOLVED:
        return {"step": user_answer.step}, 418

    return {}, 200


@app.route('/answer', methods=['POST'])
@security.protected
def answer():
    user = security.user()
    if not user:
        return {}, 401
    user_answer = user.get_answer()
    if user_answer is not None and user_answer.step == const.STEP_CAPTCHA_SOLVED:
        return {}, 403

    option = int(request.json.get('option'))

    if option not in [0, 1]:
        return {'error': f'Unknown option: {option}'}, 400

    step = const.STEP_SIMPLE_CAPTCHA
    if option == 1:
        step = const.STEP_CAPTCHA_SOLVED

    created = False
    ans = Answer.get_or_none(Answer.user == user)
    if not ans:
        created = True
        ans = Answer.create(user=user, value=option, step=step)
    if not ans:
        return {'error': 'Cannot save answer'}, 500

    if not created:
        ans.value = option
        ans.step = max(step, ans.step)
        ans.save()

    if step == const.STEP_CAPTCHA_SOLVED:
        return {}, 200
    else:
        return {"step": ans.step}, 418


def detect_lang():
    return 'ru'


def open_db_connection():
    if config.db.is_closed():
        config.db.connect(reuse_if_open=True)


def close_db_connection(response):
    if not config.db.is_closed():
        config.db.close()
    return response


app.before_request(open_db_connection)
app.after_request(close_db_connection)


if __name__ == '__main__':
    app.run()
