'''
Python module for Mopidy Pummeluff actions.
'''

__all__ = (
    'replace_tracklist',
    'set_volume',
    'play_pause',
    'stop',
    'shutdown',
)

from logging import getLogger
from os import system

LOGGER = getLogger(__name__)


def replace_tracklist(core, uri):
    '''
    Replace tracklist and play.

    :param mopidy.core.Core core: The mopidy core instance
    :param str uri: An URI for the tracklist replacement
    '''
    LOGGER.info('Replacing tracklist with URI "%s"', uri)

    playlists = [playlist.uri for playlist in core.playlists.as_list().get()]

    if uri in playlists:
        uris = [item.uri for item in core.playlists.get_items(uri).get()]
    else:
        uris = [uri]

    core.tracklist.clear()
    core.tracklist.add(uris=uris)
    core.playback.play()


def set_volume(core, volume):
    '''
    Set volume of the mixer.

    :param mopidy.core.Core core: The mopidy core instance
    :param volume: The new (percentage) volume
    :type volume: int|str
    '''
    LOGGER.info('Setting volume to %s', volume)
    try:
        core.mixer.set_volume(int(volume))
    except ValueError as ex:
        LOGGER.error(str(ex))


def play_pause(core):
    '''
    Pause or resume the playback.

    :param mopidy.core.Core core: The mopidy core instance
    '''
    playback = core.playback

    if playback.get_state().get() == 'playing':
        LOGGER.info('Pausing the playback')
        playback.pause()
    else:
        LOGGER.info('Resuming the playback')
        playback.resume()


def stop(core):
    '''
    Stop playback.

    :param mopidy.core.Core core: The mopidy core instance
    '''
    LOGGER.info('Stopping playback')
    core.playback.stop()


def shutdown(core):  # pylint: disable=unused-argument
    '''
    Shutdown.

    :param mopidy.core.Core core: The mopidy core instance
    '''
    LOGGER.info('Shutting down')
    system('sudo /sbin/shutdown -h now')
