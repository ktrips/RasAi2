#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from datetime import datetime
image_path = '/home/pi/Programs/image/'
import io
def camera():
    now = datetime.now()
    dir_name = now.strftime('%Y%m%d')
    dir_path = image_path + dir_name + '/'
    file_name= now.strftime('%H%M%S') + '.jpg'
    fname    = dir_path + file_name
    try:
      os.mkdir(dir_path)
    except OSError:
      print('Date dir already exists')
    os.system('sudo raspistill -w 640 -h 480 -o ' + fname)
    return fname

# [START vision_face_detection]
def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_face_detection]
    # [START vision_python_migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    # [END vision_python_migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        if likelihood_name[face.joy_likelihood] in ('UNLIKELY', 'VERY_UNLIKELY'):
            os.system('aplay rest.wav')
        vertices = (['({},{})'.format(vertex.x, vertex.y)
            for vertex in face.bounding_poly.vertices])
        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    # [END vision_python_migration_face_detection]
# [END vision_face_detection]


# [START vision_label_detection]
def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    # [END vision_python_migration_label_detection]
# [END vision_label_detection]


# [START vision_text_detection]
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
            for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]


def run_local(args):
    if args.command == 'faces':
        detect_faces(args.path)
    elif args.command == 'labels':
        detect_labels(args.path)
    elif args.command == 'text':
        detect_text(args.path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_faces_parser = subparsers.add_parser(
        'faces', help=detect_faces.__doc__)
    #detect_faces_parser.add_argument('path')

    detect_labels_parser = subparsers.add_parser(
        'labels', help=detect_labels.__doc__)
    #detect_labels_parser.add_argument('path')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    #detect_text_parser.add_argument('path')

    args = parser.parse_args()
    args.path = camera()

    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)
