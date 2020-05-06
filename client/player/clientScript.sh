

# mpdAdr="http://localhost:1337/videoStream/server/dash_file.mpd"
mpdAdr="http://130.245.144.102:5000/video1/dash_tiled.mpd"
# /Users/aakash/Documents/cse523/videoStream/server/dash_file.mpd
saveAdr="/Users/aakash/Documents/cse523/videoStream/"
mpdFile="dash_file.mpd"
echo "Starting downloader"
echo "*********************************************************"
echo ""

python livedownloader.py -v $mpdAdr $saveAdr
echo ""
echo "done with it. Deleting downloaded files"
rm $mpdFile

echo "*********************************************************"