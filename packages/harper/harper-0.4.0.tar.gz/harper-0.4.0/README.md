harper
======

Current version: `v0.4.0`

[![pipeline status](https://gitlab.com/jtulbright/harper/badges/master/pipeline.svg)](https://gitlab.com/jtulbright/harper/-/commits/master)
[![coverage report](https://gitlab.com/jtulbright/harper/badges/master/coverage.svg)](https://gitlab.com/jtulbright/harper/-/commits/master)


![](./docs/source/_static/harp_very_small.png)

harper is a digital signal and music library. Tooling consists of a strong base class for storing and operating on audio data (the `Signal`) as well as some common transformation and filters for digital signals. The music components of the library include some pre-defined tools for particular notes, scales, and chords.

Documentation
-------------
Available [here](https://jtulbright.gitlab.io/harper/)

Install
-------

`harper` uses `pyalsaaudio` under the hood and therefore requires
some alsa dependencies to run. On ubuntu, this is addressed
by running
> `sudo apt-get -y install libasound2-dev`

then run

>`pip install harper`


