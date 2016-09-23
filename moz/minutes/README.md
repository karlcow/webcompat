[Mozilla Web Compatibility Team](https://wiki.mozilla.org/Compatibility/Mobile#People) is having a **[weekly meeting](https://wiki.mozilla.org/Compatibility/Mobile#Minutes_and_Progress_Reports)**. We developed a few tools to edit and prepare the minutes for inserting them directly in the wikipedia wiki markup.

So far, we do

* List of new created bugs
* List of closed bugs (except duplicate)
* List of blog posts on [webcompat Planet](http://planet.webcompat.com/)

For now the Makefile is the best way to create the different parts. It could change in the future.

## Documentation

To fetch the list of open bugs and closed bugs in Web Compatibility Mobile for the last 8 days.

    make fetchdata

To modify the number of days (here 15 days)

    make fetchdata FROM=-15d

To extract the list of opened/closed bugs so it is ready to cut and paste in wiki.mozilla.org

    make open
    make closed

To extract the list of last published blog posts on planet.webcompat.com

    make feed

## Changes History

* See commits log.
* 2014-06-24: Adding a way to change the number of days.
* 2013-12-16: Adding a feature for the list of blog posts on [webcompat Planet](http://planet.webcompat.com/)