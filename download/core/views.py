import os
from pathlib import Path
import re
import yt_dlp
from rest_framework.decorators import api_view
from dataclasses import dataclass,field
from rest_framework.response import Response
from rest_framework import status



def get_download_folder ():
    """
        permet de retrouver le chemin vers le dossier de telechargement
    """
    download_folder=Path.home()/"Downloads"
    if not download_folder.exists():
        download_folder=Path.home()/"Desktop"
    print(download_folder)
    if not download_folder.exists():
        raise "Le dossier de telechargement n'existe pas..."

    return download_folder


@dataclass
class DownloadVideo:
    ydl_opts:dict=field(default_factory=dict)


    @staticmethod
    def validate_url(url):
        url_regex=(
            r'^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-.,@?^=%&:\/~+#]*)?$'
        )
        return re.match(url_regex,url) is not None


    def download_video_or_playlist(self, url: str = None,folder=None):
        if not self.validate_url(url):
            print("L'URL fournie n'est pas valide. Veuillez réessayer.")
            return
        if folder is not None:
            if os.path.exists(os.path.join(get_download_folder(),folder)):
                folder=os.path.join(get_download_folder(),folder)
            else:
                os.makedirs(os.path.join(get_download_folder(),folder))
                folder=os.path.join(get_download_folder(),folder)
        else :
            folder=get_download_folder()

        ydl_opts = self.ydl_opts
        ydl_opts['yes_playlist'] = True
        ydl_opts['outtmpl'] = f"{folder}/%(title)s.%(ext)s"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Vidéo ou playlist téléchargée avec succès")
            return Response({"code":status.HTTP_200_OK,"message":"Telechargement terminer"},status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
        return Response({"code":status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,"message":"Telechargement terminer"},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@api_view(["POST"])
def download_video(request):
    downloader=DownloadVideo()
    url=request.data['url']
    try:
        folder=request.data['folder']
    except:
        folder=None
    return downloader.download_video_or_playlist(url,folder)


@api_view(['GET'])
def get_video_title(request):
    title=None
    url=request.GET.get('url')
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title= info.get('title')
    return Response(title,status=status.HTTP_200_OK)