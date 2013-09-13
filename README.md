scripts
=======

watcher.py
----------

This uses inotify to monitor file changes.

As with `pip install pyinotify` or `apt-get install python-pyinotify` on ubuntu.

-------------------------------------------------------------------------------
> 1. It is built on:
>	https://github.com/seb-m/pyinotify
> 1. I kept the MIT license in place for that reason.
> 1. I worked from one of the tutorials provided:
>	https://github.com/seb-m/pyinotify/blob/master/python2/examples/chain.py
-------------------------------------------------------------------------------

The request was to report "all files with names starting with an underscore created under /home to $path/newfiles.log":
-------------------------------------------------------------------------------
> I assumed 
> 1. All files in the tree under /home, not just /home/filename, but anything under /home, to include /home/dir/filename/*/_file
> 1. I assumed the request meant "files", not directories that start with an underscore, but files and only files
> 1. I assumed that in real world scenarios, for example if something was going to tail /var/log/newfiles.log and act on the data there, perhaps with a logtail (http://sourceforge.net/projects/logtail/) combined with a specific code response, and since I assumed we were recursively concerned for all matching files under /home, it made sense to me to report/log the "file" as the fully qualified path for the found/matched file, and that was what I did.
-------------------------------------------------------------------------------

