import os

from maya import cmds

from .constants import MAYA_TIME_UNITS


def get_quickblast_resolution():
    """Return an image resolution based of render settings

    Returns:
        list(integer): [width, height]
    """
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")

    return [int(width), int(height)]


def get_quickblast_filename(extension: str = ".mp4"):
    """Return quickblast filename based of scene name

    Args:
        extension (str, optional): The file format extention. Defaults to ".mp4".

    Returns:
        str: The filename of the quickblast
    """
    # Get scene filename
    filepath = cmds.file(query=True, sceneName=True)
    _, filename = os.path.split(os.path.normpath(filepath))

    # Replace extension
    filename, _ = os.path.splitext(filename)

    # Check if there is a dot
    if not "." in extension:
        extension = ".%s" % extension

    return f"{filename}{extension.lower()}"


def get_quickblast_folderpath(use_workspace: bool = True):
    """Return the folder to export the quickblast

    Args:
        use_workspace (bool, optional): Use the maya workspace to generate the folderpath. Defaults to True.

    Returns:
        str: os.path like folderpath
    """
    if use_workspace:
        folderpath = os.path.normpath(cmds.workspace(fullName=True))
        folder = cmds.workspace(fileRuleEntry="movie")
        folderpath = os.path.join(folderpath, folder)

    else:
        filepath = cmds.file(query=True, sceneName=True)
        folderpath, _ = os.path.split(os.path.normpath(filepath))
        folderpath = os.path.join(folderpath, "data")

    return folderpath


def get_quickblast_framerate():
    """Return the scene framerate

    Returns:
        int: framerate in fps
    """
    time_unit = cmds.currentUnit(query=True, time=True)

    if not "fps" in time_unit:
        # Convert maya_unit labels to integer fps
        framerate = int(MAYA_TIME_UNITS[time_unit].rstrip("fps"))
    else:
        framerate = int(time_unit.rstrip("fps"))

    return framerate


def get_quickblast_soundnode():
    """Return last sound node path found in this scene

    Returns:
        str: The sound filepath
    """
    return cmds.ls(type="audio")[-1] or None


def get_quickblast_soundfile():
    """Return the filepath of the last sound node found in this scene

    Returns:
        str: os.path like
    """
    sound_node = get_quickblast_soundnode()
    return os.path.normpath(cmds.sound(sound_node, query=True, file=True)) or None


def get_sound_offset():
    """Return the sound offset relative to the start frame

    Returns:
        float: The offset in frames
    """
    sound_node = get_quickblast_soundnode()

    if sound_node:
        start_frame = cmds.playbackOptions(query=True, min=True)
        offset = cmds.sound(sound_node, query=True, offset=True)
        return offset - start_frame
    else:
        return None


def get_quickblast_duration():
    """Return the duration of the quickblast

    Returns:
        int: Duration in frames
    """
    start = cmds.playbackOptions(query=True, min=True)
    end = cmds.playbackOptions(query=True, max=True)
    return int(end - start)
