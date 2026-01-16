import os
import tempfile

import ffmpeg

from maya import cmds
from maya import OpenMaya

from quickBlast.settings import (
    get_quickblast_filename,
    get_quickblast_folderpath,
    get_quickblast_framerate,
    get_quickblast_resolution,
    get_quickblast_soundfile,
    get_quickblast_duration,
    get_sound_offset,
)

from quickBlast.sanitycheck import check_sound_node, sanitycheck


def run(show_output=True, custom_filepath=None, show_popup_errors = True):
    # Sanitycheck
    ready = sanitycheck(show_popup_errors)

    if not ready:
        OpenMaya.MGlobal.displayError("Could not run Quickblast.")
        return

    is_sound = check_sound_node()

    # Get datas
    duration = get_quickblast_duration()
    filename = get_quickblast_filename()
    folderpath = get_quickblast_folderpath()
    if custom_filepath:
        folderpath, filename = os.path.split(custom_filepath)
    framerate = get_quickblast_framerate()
    resolution = get_quickblast_resolution()
    sound_filepath = None
    sound_offset = 0
    if is_sound:
        sound_filepath = get_quickblast_soundfile()
        sound_offset = get_sound_offset()

    # Create the folderpath
    try:
        os.makedirs(folderpath)
    except OSError:
        pass

    # Do the playblast in a temporary folder
    with tempfile.TemporaryDirectory() as tmp_folder:
        # Export frames
        cmds.playblast(
            filename=os.path.join(tmp_folder, "tmp_images"),
            format="image",
            compression="jpg",
            wh=resolution,
            showOrnaments=False,
            quality=100,
            p=100,
            fo=True,
            v=False,
            fp=4,
        )

        # Get start frame
        start_frame = cmds.playbackOptions(query=True, min=True)

        # Assemble video from frames
        streams = []

        streams.append(
            ffmpeg.input(
                os.path.join(tmp_folder, "tmp_images.%04d.jpg"),
                framerate=framerate,
                start_number=start_frame,
            )
        )

        kwargs = {"filename": os.path.join(folderpath, filename)}

        if sound_filepath:
            # Get sound offset in seconds
            sound_offset = sound_offset * (1 / framerate)

            # Get duration in seconds
            duration = duration * (1 / framerate)

            streams.append(ffmpeg.input(sound_filepath, ss=-sound_offset))

            kwargs["t"] = duration

        try:
            ffmpeg.output(*streams, **kwargs).run(
                overwrite_output=True, capture_stdout=True, capture_stderr=True
            )
        except ffmpeg.Error as exception:
            print(exception.stdout.decode("UTF-8"))
            print(exception.stderr.decode("UTF-8"))
            raise exception

    if show_output:
        # Open folder with created video
        os.startfile(folderpath)
        # Open the video
        os.startfile(os.path.join(folderpath, filename))


# that's all folks #
