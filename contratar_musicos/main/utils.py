from django.utils.deconstruct import deconstructible
from uuid import uuid4
import time

import subprocess
import os
import json
import re
import gc

from django.conf import settings
from contratar_musicos.settings import MEDIA_ROOT
import datetime
import random as _random


ffprobe = "ffprobe"
ffmpeg = "ffmpeg"
media = MEDIA_ROOT
#
# if settings.IS_WEBFACTION:
#     ffmpeg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ffmpeg'))
#     ffprobe = os.path.join(ffmpeg_dir, "ffprobe")
#     # ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg")


def get_length(filename):
    file_path = os.path.join(media, filename)
    print(file_path)
    result = subprocess.Popen([ffprobe, file_path, '-print_format', 'json', '-show_streams',
                               '-loglevel', 'quiet'], stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    json_result = json.loads(result.stdout.read())
    return float(json_result['streams'][0]['duration'])


def get_video_frame(filename):
    file_path = os.path.join(media, filename)
    print(file_path)
    # infos = get_video_info(filename)
    # w, h = infos['video_size']
    """
    command = [ffmpeg,
               '-ss', '00:00:03',
               '-i', filename,
               '-f', 'image2pipe',
               '-pix_fmt', 'rgb24',
               '-vcodec', 'rawvideo', '-']
               ffmpeg -i test.avi -vcodec png -ss 10 -vframes 1 -an -f rawvideo test.png
    """
    command = [ffmpeg,
               '-i', file_path,
               # '-vcodec', 'jpeg',
               '-ss', '1',
               '-vframes', '1',
               '-an',
               '-f', 'image2pipe',
               # '-f', 'rawvideo',
               '-']  # el - al final dice que se mantiene en el pipe y no a un archivo
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10 ** 8)
    raw_image = pipe.stdout.read()
    return raw_image


def get_video_info(filename):
    command_info = [ffmpeg, '-i', filename, '-']
    pipe_info = subprocess.Popen(command_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pipe_info.stdout.readline()
    pipe_info.terminate()
    infos = pipe_info.stderr.read()

    lines = infos.splitlines()
    if "No such file or directory" in lines[-1]:
        raise IOError(("MoviePy error: the file %s could not be found !\n"
                       "Please check that you entered the correct "
                       "path.") % filename)
    result = dict()

    lines_video = [l for l in lines if ' Video: ' in l]
    result['video_found'] = (lines_video != [])
    if result['video_found']:
        try:
            line = lines_video[0]
            # get the size, of the form 460x320 (w x h)
            match = re.search(" [0-9]*x[0-9]*(,| )", line)
            s = list(map(int, line[match.start():match.end() - 1].split('x')))
            result['video_size'] = s
        except:
            raise (("MoviePy error: failed to read video dimensions in file %s.\n"
                    "Here are the file infos returned by ffmpeg:\n\n%s") % (filename, infos))
    return result


def queryset_iterator(queryset, chunksize=1000):
    """
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def ws_paginator(qs, inicio=0, cantidad=10):
    # uno mas para ver si hay otra pagina
    qs = qs[inicio:cantidad + inicio + 1]
    # vemos la cantidad real de objetos que obtuvimos
    size = len(qs)

    more = size > cantidad  # si el tamaño es mayor a lo que pidieron entonces hay otra pagina
    qs = qs[0:cantidad]
    return qs, more


def next_weekday(d, weekday):
    """
    d es una date
    weekday es el numero de dia

    esta funcion regresa la siguiente fecha que coincide con weekday
    Lunes = 0
    Domingo = 6
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def random_number(length=6, random=_random.SystemRandom(),
                  chars=list('0123456789')):
    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )


def random_mixed_string(length=16, random=_random.SystemRandom(),
                        chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789')):
    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}_{}.{}'.format(uuid4().hex, int(time.time()), ext)
        return os.path.join(self.path, filename)
