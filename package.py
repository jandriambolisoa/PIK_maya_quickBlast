name = "PIK_maya_quickBlast"

version = "0.0.4"

authors = [
    "Jeremy Andriambolisoa",
]

description = \
    """
    Quickblast is a tool to make playblast with one click.
    Uses ffmpeg and is designed for PIKTURA pipeline.
    """

requires = [
    "python-3+",
    "maya-2026+",
    "ffmpeg",
    "ffmpeg_python"
]

uuid = "piktura.PIK_maya_quickBlast"

build_command = 'python {root}/build.py {install}'

def commands():
    env.PYTHONPATH.append("{root}/python")