import string
from argparse import ArgumentParser
from glob import glob
from platform import system
from os.path import expanduser
from sqlite3 import OperationalError, connect
from typing import Optional

from django.shortcuts import render
import requests
import pytube
import instaloader
import ffmpeg
import subprocess
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import BadRequest
import builtins
from builtins import *
import time

# Create your views here.
from instaloader import BadCredentialsException, InstaloaderException, ProfileNotExistsException, \
    PrivateProfileNotFollowedException, LoginRequiredException, ConnectionException, InvalidArgumentException, \
    TwoFactorAuthRequiredException, Profile, BadResponseException, Instaloader
from pytube.exceptions import PytubeError, RegexMatchError


def index(request):
    if request.method == "POST":
        validate_url = URLValidator()
        url = request.POST.get('url').strip()
        video_resolutions = []
        try:
            yt = pytube.YouTube(url)
            if yt.streams.filter(res="1080p") != None :
                print(yt.streams.filter(res="1080p"))
                video_resolutions.append('1080')
            if yt.streams.filter(res="720p") != None :
                print(yt.streams.filter(res="720p"))
                video_resolutions.append('720')
            if yt.streams.filter(res="480p") != None :
                print(yt.streams.filter(res="480p"))
                video_resolutions.append('480')
            if yt.streams.filter(res="360p") != None :
                print(yt.streams.filter(res="360p"))
                video_resolutions.append('360')
                print(video_resolutions)
            if yt.streams.filter(res="240p") != None :
                print(yt.streams.filter(res="240p"))
                video_resolutions.append('240')
                print(video_resolutions)
            if yt.streams.filter(res="144p") != None :
                print(yt.streams.filter(res="144p"))
                video_resolutions.append('144')
                print(video_resolutions)
            for resolution in video_resolutions:
                print(resolution)

            # print(yt.streams.get_highest_resolution().resolution)
            # print(yt.streams.get_lowest_resolution().resolution)
            for stream in yt.streams.order_by('resolution'):
                print(stream)
                # print(video_resolutions.append(stream.resolution))
            yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
            audio = ffmpeg.input("audio.mp3")
            yt.streams.filter(res="720p", progressive=False).first().download(filename="video.mp4")
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
            ffmpeg.concat(video, audio, v=1, a=1).output(yttitle+".mp4").run()

            ## 720p, MERGE with COMPRESSION
            # subprocess.run('ffmpeg -i video.mp4 -i audio.mp3 -c copy -map 1:v:0? -map 0:a:0? -shortest -vcodec libx264 -vf scale=1280:720 -crf 20 -c:a aac '+ yttitle +'.mp4')

            ## Probably 720p, download video based on quality provide in ITAG
            # yt.streams.get_highest_resolution().download(r'C:\Users\PREMIUM\Downloads')

            # end = time.time()
            # maptime = (end - start) / 60
            data = {
                'url': url,
                'title': title,
                'author': author,
                'date': date,
                'view': view,
                'length': length,
                'thumbnail':thumbnail,
                # 'status': 'Video Successfully Downloaded...',
                'resolution':video_resolutions,
                # 'time': maptime
            }
            print('successfully download')
            request.session['order_id'] = 'some_id_123'
            print(request.session['order_id'])
            return render(request, 'index.html', data)
        except ValidationError as e:
            data = {'status': e}
            return render(request, 'index.html', data)
        except PytubeError as e:
            data = {'status': e}
            return render(request, 'index.html', data)
        except RegexMatchError as e:
            data = {'status': e}
            return render(request, 'index.html', data)
    else:
        # yt.streams.get_highest_resolution().download()
        return render(request, 'index.html')  # ,records

def ytvideodownload(request):
    session_id = request.session.get('order_id')
    print(request.session.get('order_id'))
    url = request.POST.get('url').strip()
    yt = pytube.YouTube(url)
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
    yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
    audio = ffmpeg.input("audio.mp3")
    yt.streams.filter(res="1080p", progressive=False).first().download(filename="video.mp4")
    video = ffmpeg.input("video.mp4")
    ffmpeg.concat(video, audio, v=1, a=1).output(yttitle + ".mp4").run()


def shorts(request):
    if request.method == "POST":
        validate_url = URLValidator()
        url = request.POST.get('url').strip()
        try:
            print(validate_url(url))
            yt = pytube.YouTube(url)
            title = yt.title
            author = yt.author
            date = yt.publish_date.strftime("%d-%m-%Y")
            view = yt.views
            length = yt.length
            data = {
                'url': url,
                'title': title,
                'author': author,
                'date': date,
                'view': view,
                'length': length,
                'status': 'Shorts Successfully Downloaded...'
            }
            yt.streams.get_highest_resolution().download()
            print('successfully download')
            return render(request, 'shorts.html', data)
        except ValidationError as e:
            data = {'status': e}
            return render(request, 'shorts.html', data)
        except PytubeError as e:
            data = {'status': e}
            return render(request, 'shorts.html', data)
        except RegexMatchError as e:
            data = {'status': e}
            return render(request, 'shorts.html', data)
    return render(request, 'shorts.html')  # ,records

ig = instaloader.Instaloader(dirname_pattern='D:\Study\BE\Summer Internship 2022\Web using Django\\testinginstaloader',compress_json=False,save_metadata=False, download_video_thumbnails=False,post_metadata_txt_pattern='')

def dp(request):
    if request.method == "POST":
        target = request.POST.get('publictarget').strip()
        try:
            # ig.login(username, password)
            target = target.split('@')[1].strip('@') if '@' in target else target
            try:
                ig.download_profile(target, profile_pic_only=True)
                data = {'status': 'Downloaded...'}
                print("data : ", data)
                return render(request, 'dp.html', data)
            # else:
            #     data = {
            #         'status': 'File already exists'
            #     }
            #     return render(request, 'dp.html', data)
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
                # 'status1': 'Internet Connection is required!',
                # 'status2': 'Instagram account checkpoint required!',
                # 'status3': 'To solve it, go to settings -> manage apps and clear all data of Instagram app.'
            }
            return render(request, 'dp.html', data)
    return render(request, 'dp.html')

def story(request):
    if request.method == "POST":
        target = request.POST.get('privatetarget').strip()
        username = request.POST.get('privateusername').strip()
        password = request.POST.get('privatepwd').strip()
        # p = ArgumentParser()


        # ig = instaloader.Instaloader()

        try:

            target = target.split('@')[1].strip('@') if '@' in target else target
            username = username.split('@')[1].strip('@') if '@' in username else username
            # p.add_argument("-c", "--cookiefile")
            # p.add_argument("-f", "--sessionfile")
            print('outside try')
            # if p.parse_args():
            #     args = p.parse_args()
            # else:
            ig.login(username, password)

            print('inside try')
            # import_session( get_cookiefile())

            print('outside 2 try')
            try:
                # ig.download_profile(target, download_stories_only=True)
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
        # except (ConnectionException, OperationalError) as e:
        #     raise SystemExit("Cookie import failed: {}".format(e))
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
        # posturl='https://www.instagram.com/p/CkN1rJRS6OQ/'
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
                            post = instaloader.Post.from_shortcode(ig.context, finalurl)
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
                    post = instaloader.Post.from_shortcode(ig.context, finalurl)
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

# def pubstory(request):
#     if request.method == "POST":
#         target = request.POST.get('privatetarget')
#         username = request.POST.get('privateusername')
#         password = request.POST.get('privatepwd')
#         # ig = instaloader.Instaloader()
#         try:
#             ig.login(username, password)
#             try:
#                 ig.download_profile(target, download_stories_only=True)
#                 data = {'status': 'Downloaded...'}
#                 print("data : ", data)
#                 return render(request, 'story.html', data)
#             except ProfileNotExistsException as e:
#                 data = {'status': e}
#                 return render(request, 'story.html', data)
#             except PrivateProfileNotFollowedException as e:
#                 data = {'status': e}
#                 return render(request, 'story.html', data)
#         except InvalidArgumentException as e:
#             data = {'status': e}
#             return render(request, 'story.html', data)
#         except TwoFactorAuthRequiredException as e:
#             data = {'status': e}
#             return render(request, 'story.html', data)
#         except BadCredentialsException as e:
#             data = {'status': 'Provide Valid Username and Password'}
#             return render(request, 'story.html', data)
#         except LoginRequiredException as e:
#             data = {'status': e}
#             return render(request, 'story.html', data)
#         except ConnectionException as e:
#             data = {'status': e}
#             return render(request, 'story.html', data)
#     return render(request, 'story.html')


'''
# def puballpost(request):
#     return render(request, 'puballpost.html')


def pridp(request):
    if request.method == "POST":
        target = request.POST.get('pridptarget')
        username = request.POST.get('pridpusername')
        password = request.POST.get('pridppwd')
        # ig = instaloader.Instaloader()
        try:
            ig.login(username, password)
            try:
                ig.download_profile(target, profile_pic_only=True)
                data = {'status': 'Downloaded...'}
                print("data : ", data)
                return render(request, 'pridp.html', data)
            # else:
            #     data = {
            #         'status': 'File already exists'
            #     }
            #     return render(request, 'pridp.html', data)
            except ProfileNotExistsException as e:
                data = {'status': e}
                return render(request, 'pridp.html', data)
            except PrivateProfileNotFollowedException as e:
                data = {'status': e}
                return render(request, 'pridp.html', data)
        except InvalidArgumentException as e:
            data = {'status': e}
            return render(request, 'pridp.html', data)
        except BadCredentialsException as e:
            data = {'status': 'Provide Valid Username and Password'}
            return render(request, 'pridp.html', data)
        except LoginRequiredException as e:
            data = {'status': e}
            return render(request, 'pridp.html', data)
        except ConnectionException as e:
            data = {
                'status':e,
                # 'status1': 'Internet Connection is required!',
                # 'status2': 'Instagram account checkpoint required!',
                # 'status3': 'To solve it, go to settings -> manage apps and clear all data of Instagram app.'
            }
            return render(request, 'pridp.html', data)
    return render(request, 'pridp.html')
 '''

# def pristory(request):
#     return render(request, 'pristory.html')


# def pripost(request):
#     return render(request, 'pripost.html')
#
#
# def priallpost(request):
#     return render(request, 'priallpost.html')

def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)
