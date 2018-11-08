
# Daily Use

* [Organisation](#organisation)
* [Diary](#diary)
* [Monitoring](#monitoring)
  * [Download from Garmin Connect](#download-from-garmin-connect)
  * [Monitor Entry](#monitor-entry)
* [Activities](#activities)
  * [Download from Device](#download-from-device)
  * [Activity Entry](#activity-entry)

## Organisation

It makes a lot of sense to keep *all* your FIT data on disk somewhere.
This way, if something changes in Choochoo and the database becomes
invalid / needs chancging, you can re-load the data rather than trying
to port the old database.

Also, keeping your FIT data means you're not tied to using Choochoo in
the future.

The program has been designed with this in mind - it will re-scan
directories containing FIT data and only processs data that are new.

So before starting, choose where you will store FIT data (and maybe
make backup copies of this data on a regular basis, along with the
Choochoo database).

## Diary

Starting the diary with

    > ch2 diary

will display the configured topic fields for data entry (for today).
When you are done, type `alt-Q` to save and quite (`alt-X` to quite
without saving).

You can choose alternative dates by specifying a date on the command
line or by `alt-D/W/M/Y` to move (backwards) by a day / week / month
/year.  To move forwards hold down `shift` too.  To move to the last
activity use `alt-A`.

See [configuration(configuration) for how to add additional fields.

## Monitoring

Monitoring refers to "lifetyle" data collected by Garmin (or
compatible) watches.  In particular, heart rate and steps walked are
recorded.

### Download from Garmin Connect

Each morning I upload monitor data to Garmin Connect using the phone
app.  This tells me how many hours I slept, number of steps I walked
previous day, etc.

To get the data into Choochoo we need to download it from Garmin.
There are two ways to do this.

The first time you download data, you probably have a *lot* of data to
download.  So go to
[https://www.garmin.com/en-US/account/datamanagement/](https://www.garmin.com/en-US/account/datamanagement/)
and download all the data.  Unpack this into a suitable directory so
that the FIT files are visible.

Subsequent times you download data, you probably only have a day or
two of data to download.  In this case use the command

    > ch2 garmin --user USER --pass PWD PATH/TO/DIR

to download the latest data.

### Monitor Entry

Once you have downloaded the data it can be read into Choochoo using

    > ch2 monitor PATH/TO/DATA

If you enable multi-directory globbing (`shopt -s globstar` in bash)
then the command might look like:

    > ch2 monitor /archive/**/*.fit

This will load data and re-calculate appropriate statistics.

## Activities

Activities are things like bike rides, runs, etc.  These are grouped
by 'activity groups' which are part of the
[configuration](configuration).

### Download from Device

After an activity I connect my watch to the computer using USB and
download the FIT file with data to disk.

(In future it should also be possible to download from Garmin Connect
- I haven't needed this yet, so haven't written the code).

Data from previous activities may be avaialble to download in bulk
from Starava, Garmin, etc.

### Activity Entry

Once you have downloaded the data it can be read into Choochoo using

    > ch2 activities PATH/TO/DATA

If you enable multi-directory globbing (`shopt -s globstar` in bash)
then the command might look like:

    > ch2 activities /archive/**/*.fit

This will load data and re-calculate appropriate statistics.

