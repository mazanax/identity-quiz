import requests

import config


def vk_token(code):
    raw_response = requests.get('https://oauth.vk.com/access_token', params={
        'client_id': config.vk_client_id,
        'client_secret': config.vk_client_secret,
        'redirect_uri': f'{config.site_host}/auth/vk',
        'code': code,
    })
    response = raw_response.json()

    if response.get('error', None) is not None:
        config.logger.error(f'[VK AUTH]: {response.get("error")}')
        raise RuntimeError

    user_id = int(response.get('user_id', None))
    token = response.get('access_token')

    return user_id, token


def fb_token(code):
    raw_response = requests.get('https://graph.facebook.com/v9.0/oauth/access_token', params={
        'client_id': config.fb_client_id,
        'client_secret': config.fb_client_secret,
        'redirect_uri': f'{config.site_host}/auth/facebook',
        'code': code,
        'scope': 'email'
    })
    response = raw_response.json()

    if not (token := response.get('access_token')):
        config.logger.error(f'[FB AUTH]: {response.get("error").get("message")}')
        raise RuntimeError

    raw_response = requests.get('https://graph.facebook.com/v9.0/me', params={
        'fields': 'email',
        'access_token': token
    })
    response = raw_response.json()

    return response.get('id'), token


def google_token(code):
    raw_response = requests.post('https://oauth2.googleapis.com/token', params={
        'code': code,
        'redirect_uri': f'{config.site_host}/auth/google',
        'client_id': config.google_client_id,
        'client_secret': config.google_client_secret,
        'grant_type': 'authorization_code'
    })
    response = raw_response.json()

    if not (token := response.get('access_token')):
        config.logger.error(f'[GOOGLE AUTH]: {response}')
        raise RuntimeError

    raw_response = requests.post('https://openidconnect.googleapis.com/v1/userinfo', params={
        'access_token': token
    })
    response = raw_response.json()

    return response.get('sub'), token


def get_user_name(provider, user_id, token):
    if provider == 'vk':
        return vk_user_name(user_id, token)
    if provider == 'facebook':
        return fb_user_name(token)
    if provider == 'google':
        return google_user_name(token)

    return ''


def vk_user_name(user_id, token):
    raw_response = requests.get('https://api.vk.com/method/users.get', params={
        'users_id': user_id,
        'v': 5.126,
        'access_token': token,
    })
    response = raw_response.json()
    if response.get('response', None) is not None:
        user_info = response.get('response')[0]
        name = '{} {}'.format(user_info['first_name'], user_info['last_name'])

        return name
    return ''


def fb_user_name(token):
    raw_response = requests.get('https://graph.facebook.com/v9.0/me', params={
        'fields': 'name',
        'access_token': token
    })
    response = raw_response.json()
    name = response.get('name')

    return name or ''


def google_user_name(token):
    raw_response = requests.post('https://openidconnect.googleapis.com/v1/userinfo', params={
        'access_token': token
    })
    response = raw_response.json()

    return response.get('name')
