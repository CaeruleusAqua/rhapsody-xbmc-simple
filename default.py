import sys
import xbmcgui
import urllib
import xbmc
import urlparse
import xbmcplugin
import xbmcaddon
import xbmcgui
from lib.main import Application

my_addon = xbmcaddon.Addon()

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'audio')

app = Application()

app.mem.username=my_addon.getSetting('username')
app.mem.password=my_addon.getSetting('password')

print app.mem.username
print app.mem.password


mode = args.get('mode', None)


if not app.mem.has_saved_creds():
    ret = app.mem.login_member(name=app.mem.username,pswd=app.mem.password)
    if ret["logged_in"]==False:
        mode = ['exit']
        if ret["bad_creds"]:
            dialog = xbmcgui.Dialog()
            dialog.ok("bad credentials","Wrong username or password!")
        else:
            xbmcgui.Dialog.notification("Error","error during login",xbmcgui.NOTIFICATION_ERROR)



    app.mem.save_user_info()


playlist=None

player = xbmc.Player()

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

genres = app.api.get_genres()

def viewArtists(artists):
    for artist in artists:
        li = xbmcgui.ListItem(artist['name'])
        li.setLabel2(artist['name'])
        li.setLabel(artist['name'])
        li.setThumbnailImage(app.cache.getArtistImage(artist['id']))
        url = build_url({'mode': 'artist', 'name': artist['id']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def viewAlbums(albums):
    for album in albums:
        li = xbmcgui.ListItem(album['name'])
        li.setLabel2(album['artist']['name'])
        li.setLabel(album['name'])
        li.setInfo('music', { 'album': album['name'],
                   'artist': album['artist']['name'] })
        li.setThumbnailImage(app.cache.getAlbumImage(album['id']))
        url = build_url({'mode': 'album', 'name': album['id']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def viewTracks(tracks):
    for track in tracks:
        li = xbmcgui.ListItem(track['name'])
        li.setProperty('IsPlayable', 'true')
        li.setInfo('music', {'title': track['name'],
                             'album': track['album']['name'],
                             'duration': track['duration'],
                             'genre': app.cache.getGenre(track['genre']['id'])['name'],
                             'artist': track['artist']['name'] })
        li.setThumbnailImage(app.cache.getAlbumImage(track['album']['id']))
        url = build_url({'mode': 'track', 'name': track['id']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)


def viewPlaylists(playlists):
    for playlist in playlists:
        li = xbmcgui.ListItem(playlist['name'])
        url = build_url({'mode': 'playlist', 'name': playlist['id']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)





if mode is None:
    url = build_url({'mode': 'search', 'name': 'None'})
    li = xbmcgui.ListItem('Suche', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)



    url = build_url({'mode': 'top_tracks'})
    li = xbmcgui.ListItem('Top Titel', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'top_album'})
    li = xbmcgui.ListItem('Top Alben', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'top_artists'})
    li = xbmcgui.ListItem('Top Interpreten', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'top_playlists'})
    li = xbmcgui.ListItem('Top Playlists', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)



    url = build_url({'mode': 'info'})
    li = xbmcgui.ListItem('Account Info', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'search':
    if args['name'][0] == 'None':
        url = build_url({'mode': 'search', 'name': 'artist'})
        li = xbmcgui.ListItem('Interpret', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        url = build_url({'mode': 'search', 'name': 'album'})
        li = xbmcgui.ListItem('Titel', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        url = build_url({'mode': 'search', 'name': 'track'})
        li = xbmcgui.ListItem('Album', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        url = build_url({'mode': 'search', 'name': 'playlist'})
        li = xbmcgui.ListItem('Playlist', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        url = build_url({'mode': 'search', 'name': 'latest'})
        li = xbmcgui.ListItem('Zuletzt Gesucht', iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)

    elif args['name'][0] == 'artist':
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            search_string = keyboard.getText().replace(" ", "+")
            app.cache.saveSearch(search_string,'artist')
            result = app.api.get_search_results(search_string,"artist")
            viewArtists(result)

    elif args['name'][0] == 'album':
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            search_string = keyboard.getText().replace(" ", "+")
            app.cache.saveSearch(search_string,'album')
            result = app.api.get_search_results(search_string,"album")
            viewAlbums(result)

    elif args['name'][0] == 'track':
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            search_string = keyboard.getText().replace(" ", "+")
            app.cache.saveSearch(search_string,'track')
            result = app.api.get_search_results(search_string,"track")
            viewTracks(result)

    elif args['name'][0] == 'playlist':
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            search_string = keyboard.getText().replace(" ", "+")
            app.cache.saveSearch(search_string,'playlist')
            result = app.api.get_search_results(search_string,"playlist")
            viewPlaylists(result)

    elif args['name'][0] == 'latest':
        search = app.cache.getSearch()
        for i in search:
            url = build_url({'mode': 'search_latest', 'param0': i[0], 'param1': i[1]})
            li = xbmcgui.ListItem(i[0], iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'search_latest':
    result = app.api.get_search_results(args['param0'][0],args['param1'][0])
    if args['param1'][0] == 'artist':
        viewArtists(result)

    elif args['param1'][0] == 'album':
        viewAlbums(result)

    elif args['param1'][0] == 'track':
        viewTracks(result)

    elif args['param1'][0] == 'playlist':
        viewPlaylists(result)


elif mode[0] == 'top_artists':
    artists = app.api.get_top_artists()
    viewArtists(artists)

elif mode[0] == 'artist':
    albums = app.api.get_discography(args['name'][0])
    viewAlbums(albums)

elif mode[0] == 'top_album':
    albums = app.api.get_top_albums()
    viewAlbums(albums)

elif mode[0] == 'album':
    tracks = app.api.get_album_tracks(args['name'][0])
    viewTracks(tracks)

elif mode[0] == 'top_playlists':
    playlists = app.api.get_featured_playlists()
    viewPlaylists(playlists)


elif mode[0] == 'playlist':
    tracks = app.api.get_playlist_tracks(args['name'][0])
    viewTracks(tracks)

elif mode[0] == 'info':
    account_info = app.api.get_account_info()
    li = xbmcgui.ListItem("Login: " + account_info['logon'])
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=None, listitem=li)
    li = xbmcgui.ListItem("Katalog: " + account_info['catalog'])
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=None, listitem=li)
    li = xbmcgui.ListItem("Anbieter: " + account_info['billingPartnerCode'])
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=None, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'top_tracks':
    viewTracks(app.api.get_top_tracks())



elif mode[0] == 'track':
    id = args['name'][0]
    url=app.api.get_playable_url(id)
    if url is not False:
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
        pass
        #player.stop()
        #xbmcgui.Dialog().ok("Error","test","test","test",)

elif mode[0] == 'exit':
    print "terminated"


print "RUNnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"