# twitter
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# user profile
from twitterauth.models import Profile

from django.conf import settings

import oauth2 as oauth
import twitter
import cgi

# twitter constants
# twitter auth

if not settings.DEBUG:
    TWITTER_TOKEN = 'qCDMfzY7EwYYvfexCRU0g'
    TWITTER_SECRET = 'XaKiXHIiSWvfAAxRfnPOD7anvEdQvL2Dkkp5uv8UU4'
else:
    TWITTER_TOKEN = 'Jgv5yKceI2hl7t2v1zhDwA'
    TWITTER_SECRET = 'OzIAPLSxlwnGX4V8iSl2eXD9VFS65EwjTlfLpgNaAEE'

consumer = oauth.Consumer(TWITTER_TOKEN, TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'

# This is the slightly different URL used to authenticate/authorize.
authenticate_url = 'http://twitter.com/oauth/authenticate'


def twitter_data(token, token_secret):
    """ Returns the current user information """

    api = twitter.Api(consumer_key=TWITTER_TOKEN,
                      consumer_secret=TWITTER_SECRET,
                      access_token_key=token,
                      access_token_secret=token_secret)

    return api.VerifyCredentials()


def twitter_login(request):
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

    return HttpResponseRedirect(url)


@login_required
def twitter_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect(reverse('clips:talks'))


def twitter_authenticated(request):
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        print content
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797',
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))

    # Step 3. Lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        # When creating the user I just use their screen_name@twitter.com
        # for their email and the oauth_token_secret for their password.
        # These two things will likely never be used. Alternatively, you
        # can prompt them for their email here. Either way, the password
        # should never be used.
        user = User.objects.create_user(access_token['screen_name'],
            '%s@twitter.com' % access_token['screen_name'],
            access_token['oauth_token_secret'])

    # if the user does not have a profile, lets create it
    if not user.profile_set.count():
        # Save our permanent token and secret for later.
        profile = Profile()

        # update profile info
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    # Authenticate the user and log them in using Django's pre-built
    # functions for these things.
    user = authenticate(username=access_token['screen_name'],
                        password=access_token['oauth_token_secret'])

    if user is not None:
        login(request, user)

    return HttpResponseRedirect(reverse('clips:talks'))
