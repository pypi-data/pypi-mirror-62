# wpx 💻

Wpx is a wallpaper downloader. That's it.

##### Supported Wallpaper Providers

* [Bing.com](https://www.bing.com/)
* [WallpapersHome](https://wallpapershome.com)

##### Usage

Get Bing's image of the day:

    $ FILENAME=$(wpx bing -d ~/Pictures/wallpapers --daily)

Get a random image from a WallpapersHome category:

    $ FILENAME=$(wpx wallpapershome '{category: art/anime}' --random)
