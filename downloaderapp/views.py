import string
from argparse import ArgumentParser
from glob import glob
from platform import system
from os.path import expanduser
from sqlite3 import OperationalError, connect
from typing import Optional

from django.shortcuts import render
import subprocess
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import BadRequest
import builtins
from builtins import *
import time

# Create your views here.

def index(request):
    if request.method == "POST":
        validate_url = URLValidator()
        url = request.POST.get('url').strip()
        try:
            yt = YouTube(url)
            
            yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
            audio = ffmpeg.input("audio.mp3")
            yt.streams.filter(res="1080p", progressive=False).first().download(filename="video.mp4")
            video = ffmpeg.input("video.mp4")

            title = yt.title
            author = yt.author
            date = yt.publish_date.strftime("%d-%m-%Y")
            view = yt.views
            length = yt.length
            thumbnail = yt.thumbnail_url

            char_to_replace = {'|': '',
                               '/': '',
                               '\\': '',
                               '?': '',
                               ':': '',
                               '*': '',
                               '>': '',
                               '<': '',
                               '"': '',
                               ' ': ''}
            yttitle = str(yt.title.translate(str.maketrans(char_to_replace)))

            # start = time.time()

            ## HD 1080p, Only Merge Video and Audio, without Compression
            ffmpeg.concat(video, audio, v=1, a=1).output(yttitle).run()

            data = {
                'url': url,
                'title': title,
                'author': author,
                'date': date,
                'view': view,
                'length': length,
                'thumbnail':thumbnail,
                'status': 'Video Successfully Downloaded...',
                'resolution':video_resolutions,
            }
            print('successfully download')
            request.session['order_id'] = 'some_id_123'
            print(request.session['order_id'])
            return render(request, 'index.html', data)
        except ValidationError as e:
            data = {'status': e}
            return render(request, 'index.html', data)
        except Error as e:
            data = {'status': e}
            return render(request, 'index.html', data)
        except RegexMatchError as e:
            data = {'status': e}
            return render(request, 'index.html', data)
    else:
        return render(request, 'index.html')

def dp(request):
    if request.method == "POST":
        target = request.POST.get('publictarget').strip()
        try:
            target = target.split('@')[1].strip('@') if '@' in target else target
            try:
                ig.download_profile(target, profile_pic_only=True)
                data = {'status': 'Downloaded...'}
                print("data : ", data)
                return render(request, 'dp.html', data)
            except ProfileNotExistsException as e:
                data = {'status': e}
                return render(request, 'dp.html', data)
            except PrivateProfileNotFollowedException as e:
                data = {'status': e}
                return render(request, 'dp.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'dp.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'dp.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'dp.html', data)
        except ConnectionException as e:
            data = {
                'status':e,
            }
            return render(request, 'dp.html', data)
    return render(request, 'dp.html')

def story(request):
    if request.method == "POST":
        target = request.POST.get('privatetarget').strip()
        username = request.POST.get('privateusername').strip()
        password = request.POST.get('privatepwd').strip()
        try:
            target = target.split('@')[1].strip('@') if '@' in target else target
            username = username.split('@')[1].strip('@') if '@' in username else username
            ig.login(username, password)
            try:
                profile = Profile.from_username(ig.context, target)
                ig.download_stories(userids=[profile.userid], filename_target='{}/stories'.format(profile.username))
                data = {'status': 'Downloaded...'}
                print("data : ", data)
                return render(request, 'story.html', data)
            except ProfileNotExistsException as e:
                data = {'status': e}
                return render(request, 'story.html', data)
            except PrivateProfileNotFollowedException as e:
                data = {'status': e}
                return render(request, 'story.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'story.html', data)
        except TwoFactorAuthRequiredException as e:
            data = {'status': e}
            return render(request, 'story.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'story.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'story.html', data)
        except ConnectionException as e:
            data = {'status': e}
            return render(request, 'story.html', data)
    return render(request, 'story.html')

def singlepost(request):
    if request.method == "POST":
        posturl = request.POST.get('igpublicpost').strip()
        username = request.POST.get('privateusername').strip()
        print(username)
        password = request.POST.get('privatepwd').strip()
        validate_url = URLValidator()
        try:
            if posturl != None:
                username = username.split('@')[1].strip('@') if '@' in username else username
                validate_url(posturl)
                print(validate_url(posturl))
                ig.login(username, password)
                try:
                            trimurl = (posturl.split('/p/')[1].strip('/ ')) #perform left slice(trim) of url
                            finalurl= trimurl.split('/?')[0].strip('/ ') #perform right slice(trim) of url
                            post = Post.from_shortcode(ig.context, finalurl)
                            ig.download_post(post,username)
                            data = {'status': 'Downloaded...'}
                            print("data : ", data)
                            return render(request, 'singlepost.html', data)
                except IndexError as e:
                            data = {'status': e}
                            return render(request, 'singlepost.html', data)
                except ProfileNotExistsException as e:
                            data = {'status': e}
                            return render(request, 'singlepost.html', data)
                except BadResponseException  as e:
                            data = {'status': 'Enter valid URL and User Name!'}
                            return render(request, 'singlepost.html', data)
                except PrivateProfileNotFollowedException as e:
                            data = {'status': e}
                            return render(request, 'singlepost.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'singlepost.html', data)
        except ValidationError as e:
            data = {'status': e}
            return render(request, 'singlepost.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'singlepost.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'singlepost.html', data)
        except ConnectionException as e:
            data = { 'status': e}
            return render(request, 'singlepost.html', data)
    return render(request, 'singlepost.html')

def allpost(request):
    if request.method == "POST":
        target = request.POST.get('privatetarget').strip()
        username = request.POST.get('privateusername').strip()
        password = request.POST.get('privatepwd').strip()
        try:
            target = target.split('@')[1].strip('@') if '@' in target else target
            username = username.split('@')[1].strip('@') if '@' in username else username
            ig.login(username, password)
            try:
                ig.download_profile(target)
                # profile = Profile.from_username(ig.context, target)
                # ig.download_stories(userids=[profile.userid], filename_target='{}/stories'.format(profile.username))
                data = {'status': 'Downloaded...'}
                print("data : ", data)
                return render(request, 'allpost.html', data)
            except ProfileNotExistsException as e:
                data = {'status': e}
                return render(request, 'allpost.html', data)
            except PrivateProfileNotFollowedException as e:
                data = {'status': e}
                return render(request, 'allpost.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'allpost.html', data)
        except TwoFactorAuthRequiredException as e:
            data = {'status': e}
            return render(request, 'allpost.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'story.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'allpost.html', data)
        except ConnectionException as e:
            data = {'status': e}
            return render(request, 'allpost.html', data)
    return render(request, 'allpost.html')

def reels(request):
    if request.method == "POST":
        posturl = request.POST.get('igpublicreels').strip()
        username = request.POST.get('privateusername').strip()
        password = request.POST.get('privatepwd').strip()
        validate_url = URLValidator()
        try:
            if posturl != None:
                validate_url(posturl)
                print(validate_url(posturl))
                username = username.split('@')[1].strip('@') if '@' in username else username
                ig.login(username, password)
                try:
                    trimurl = (posturl.split('/reel/')[1].strip('/ '))  # perform left slice(trim) of url
                    finalurl = trimurl.split('/?')[0].strip('/ ')  # perform right slice(trim) of url
                    post = Post.from_shortcode(ig.context, finalurl)
                    ig.download_post(post, username)
                    data = {'status': 'Downloaded...'}
                    print("data : ", data)
                    return render(request, 'reels.html', data)
                except IndexError as e:
                    data = {'status': e}
                    return render(request, 'reels.html', data)

                except ProfileNotExistsException as e:
                    data = {'status': e}
                    return render(request, 'reels.html', data)
                except BadResponseException as e:
                    data = {'status': 'Enter valid URL and User Name!'}
                    return render(request, 'reels.html', data)
                except PrivateProfileNotFollowedException as e:
                    data = {'status': e}
                    return render(request, 'reels.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'reels.html', data)
        except ValidationError as e:
            data = {'status': e}
            return render(request, 'reels.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'reels.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'reels.html', data)
        except ConnectionException as e:
            data = {'status': e}
            return render(request, 'reels.html', data)
    return render(request, 'reels.html')
