#!/usr/bin/env python3
import os, argparse
from pathlib import Path
from time import time
from glitch_this import ImageGlitcher

def islatest(version):
    # Check pypi for the latest version number
    from urllib import request
    import json
    try:
        contents = request.urlopen('https://pypi.org/pypi/glitch-this/json').read()
    except:
        # Connection issue
        # Silenty return True, update check failed
        return True
    data = json.loads(contents)
    latest_version = data['info']['version']

    return version == latest_version

def get_help(glitch_min, glitch_max):
    help_text = dict()
    help_text['path'] = 'Relative or Absolute string path to source image'
    help_text['level'] = """
                          Integer between {} and {}, inclusive,
                          representing amount of glitchiness
                         """.format(glitch_min, glitch_max)
    help_text['color'] = 'Whether or not to add color offset\nDefaults to False'
    help_text['scan'] = 'Whether or not to add scan lines effect\nDefaults to False'
    help_text['gif'] = """
                        Include if you want a GIF instead of static image
                        NOTE: Does nothing if input image is GIF, i.e when using `-ig`
                       """
    help_text['frames'] = """
                           How many frames to include in GIF
                           Defaults to 23
                           NOTE: Does nothing if input image is GIF, i.e when using `-ig`
                          """
    help_text['step'] = """
                         If provided, will glitch every step'th frame
                         Defaults to 1, i.e glitch all frames
                         Only works if -ig or -g is included
                        """
    help_text['increment'] = """
                              Increment glitch_amount by given value after glitching every frame
                              Defaults to 0
                              NOTE: Only works when creating glitched GIFs
                             """
    help_text['cycle'] = """
                          Cycle glitch_amount back to {} or {} if it over/underflows
                          Defaults to False, i.e glitch_amount will stay at {}/{} if it under/overflows
                         """.format(glitch_min, glitch_max, glitch_min, glitch_max)
    help_text['duration'] = 'How long to display each frame (in centiseconds), defaults to 200'
    help_text['relative_duration'] = """
                                      Use a duration relative to the input GIF's original duration
                                      The given value is multiplied by the input GIF's original duration
                                      If a value is provided, -d Duration is ignored
                                      NOTE: Only works with -ig param
                                     """
    help_text['loop'] = 'How many times the glitched GIF should loop, defaults to 0 (i.e infinite loop)'
    help_text['inputgif'] = """
                             If input image is GIF, use for glitching GIFs to GIFs!
                             Defaults to False
                             NOTE: This is a slow process
                            """
    help_text['force'] = """
                          If included, overwrites existing output file of same name (if found)
                          Defaults to False
                         """
    help_text['out'] = """
                        Explictly supply the full or relative path/filename
                        Defaults to ./glitched_src_image_path
                       """
    return help_text

def main():
    glitch_min, glitch_max = 1, 10
    help_text = get_help(glitch_min, glitch_max)
    # Add commandline arguments parser
    argparser = argparse.ArgumentParser(description='Glitchify images to static images and GIFs!')
    argparser.add_argument('src_img_path', metavar='Image_Path', type=str,
                           help=help_text['path'])
    argparser.add_argument('glitch_level', metavar='Glitch_Level', type=int,
                           help=help_text['level'])
    argparser.add_argument('-c', '--color', dest='color', action='store_true',
                           help=help_text['color'])
    argparser.add_argument('-s', '--scan', dest='scan_lines', action='store_true',
                           help=help_text['scan'])
    argparser.add_argument('-g', '--gif', dest='gif', action='store_true',
                           help=help_text['gif'])
    argparser.add_argument('-fr', '--frames', dest='frames', metavar='Frames', type=int, default=23,
                           help=help_text['frames'])
    argparser.add_argument('-st', '--step', dest='step', metavar='Step', type=int, default=1,
                           help=help_text['step'])
    argparser.add_argument('-i', '--increment', dest='increment', metavar='Increment', type=int, default=0,
                           help=help_text['increment'])
    argparser.add_argument('-cy', '--cycle', dest='cycle', action='store_true',
                           help=help_text['cycle'])
    argparser.add_argument('-d', '--duration', dest='duration', metavar='Duration', type=int, default=200,
                           help=help_text['duration'])
    argparser.add_argument('-rd', '--relative_duration', dest='rel_duration', metavar='Relative_Duration', type=float,
                           help=help_text['relative_duration'])
    argparser.add_argument('-l', '--loop', dest='loop', metavar='Loop_Count', type=int, default=0,
                           help=help_text['loop'])
    argparser.add_argument('-ig', '--inputgif', dest='input_gif', action='store_true',
                           help=help_text['inputgif'])
    argparser.add_argument('-f', '--force', dest='force', action='store_true',
                           help=help_text['force'])
    argparser.add_argument('-o', '--outfile', dest='outfile', metavar='Outfile_path', type=str,
                           help=help_text['out'])
    args = argparser.parse_args()

    # Sanity check inputs
    if not args.duration > 0:
        raise ValueError('Duration must be greater than 0')
    if not args.loop >= 0:
        raise ValueError('Loop must be greater than or equal to 0')
    if not args.frames > 0:
        raise ValueError('Frames must be greater than 0')
    if not os.path.isfile(args.src_img_path):
        raise FileNotFoundError('No image found at given path')

    # Set up full_path, for output saving location
    out_path, out_file = os.path.split(Path(args.src_img_path))
    out_filename, out_fileex = out_file.rsplit('.', 1)
    out_filename = 'glitched_' + out_filename
    # Output file extension should be '.gif' if output file is going to be a gif
    out_fileex = 'gif' if args.gif else out_fileex
    if args.outfile:
        # If output file path is already given
        # Overwrite the previous values
        out_path, out_file = os.path.split(Path(args.outfile))
        if out_path != '' and not os.path.exists(out_path):
            raise Exception('Given outfile path, ' + out_path + ', does not exist')
        # The extension in user provided outfile path is ignored
        out_filename = out_file.rsplit('.', 1)[0]
    # Now create the full path
    full_path = os.path.join(out_path, '{}.{}'.format(out_filename, out_fileex))
    if os.path.exists(full_path) and not args.force:
        raise Exception(full_path + ' already exists\nCannot overwrite '
                        'existing file unless -f or --force is included\nProgram Aborted')

    # Actual work begins here
    glitcher = ImageGlitcher()
    t0 = time()
    if not args.input_gif:
        # Get glitched image or GIF (from image)
        glitch_img = glitcher.glitch_image(args.src_img_path, args.glitch_level,
                                           glitch_change=args.increment,
                                           cycle=args.cycle,
                                           scan_lines=args.scan_lines,
                                           color_offset=args.color,
                                           gif=args.gif,
                                           frames=args.frames,
                                           step=args.step)
    else:
        # Get glitched image or GIF (from GIF)
        glitch_img, src_duration, args.frames = glitcher.glitch_gif(args.src_img_path, args.glitch_level,
                                                                    glitch_change=args.increment,
                                                                    cycle=args.cycle,
                                                                    scan_lines=args.scan_lines,
                                                                    color_offset=args.color,
                                                                    step=args.step)
        # Set args.gif to true if it isn't already in this case
        args.gif = True
        # Set args.duration to src_duration * relative duration, if one was given
        args.duration = args.duration if not args.rel_duration else int(args.rel_duration * src_duration)
    t1 = time()
    # End of glitching
    t2 = time()
    # Save the image
    if not args.gif:
        glitch_img.save(full_path, compress_level=3)
        t3 = time()
        print('Glitched Image saved in "{}"'.format(full_path))
    else:
        glitch_img[0].save(full_path,
                    format='GIF',
                    append_images=glitch_img[1:],
                    save_all=True,
                    duration=args.duration,
                    loop=args.loop,
                    compress_level=3)
        t3 = time()
        print('Glitched GIF saved in "{}"\nFrames = {}, Duration = {}, Loop = {}'.format(full_path, args.frames, args.duration, args.loop))
    print('Time taken to glitch: ' + str(t1 - t0))
    print('Time taken to save: ' + str(t3 - t2))
    print('Total Time taken: ' + str(t3 - t0))

    # Let the user know if new version is available
    if not islatest(ImageGlitcher.__version__):
        print('A new version of "glitch-this" is available. Please consider upgrading via `pip install --upgrade glitch-this`')

if __name__=='__main__':
    main()
