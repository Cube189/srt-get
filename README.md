# srt-get (WIP)

A CLI program for downloading movie subtitles.


## Usage

Assuming you placed the source code in a file named `srt-get`
and made it globally executable (if you don't understand, see
"Installation" below).

```
srt-get movie-name subtitle-language
```

A `.zip` archive with a subtitle file will be placed in
the directory you ran the command from.


## "Installation"

Before your first time with this script, consider running 
this little bit of Bash below in the same directory you have
the script file in.

```
if which python > /dev/null; then
    chmod a+x srt-get;
    mv srt-get /usr/local/bin/srt-get;
else
    echo "You need to have Python installed";
    echo "https://www.python.org/downloads/";
fi
```

Now the script can be executed from everywhere. Yay! &#1f64c; 