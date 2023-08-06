# Parsing binary .wfm files created by Rigol scopes

## Background

This project is should be a one-stop location for interpreting waveform `.wmf` files from any Rigol scopes.  Programs that parse Rigol's binary `.wfm` files are sadly balkanized: each project tends to support a single scope model and the available efforts are spread across a wide range of languages.

Most seem to avoid do not deal specifically with the `.wfm` format and if they do, then only one specific scope model is supported.

Initially, I too, was only interested in a single scope format (DS1102E) and I successfully used the python parser written by Blaicher <https://github.com/mabl/pyRigolWFM>.  Later, I noticed that 1000Z files were supported by the Szkutnik  <https://github.com/michal-szkutnik/pyRigolWfm1000Z> and added support for these scopes.  Later, I found the DS1000D Matlab code by Wagenaars <https://www.mathworks.com/matlabcentral/fileexchange/18999-read-binary-rigol-waveforms>.
Eventually, I ran across the work on DS4000 files by Cat-Ion <https://github.com/Cat-Ion/rigol-ds4000-wfm>.

This last project leveraged Kaitai Struct <https://kaitai.io> as a domain specific language to represent the binary files.  Once the binary waveform files have been described as a `.ksy` files then parsers can be generated for a wide range of languages (C++/STL, C#, Go, Java, JavaScript, Lua, Perl, PHP, Python, and Ruby).  Moreover, Kaitai Struct has a Web IDE <https://ide.kaitai.io> that allows one to interactively reverse engineer binary file formats.  This is super helpful for those Rigol `.wfm` formats that are undocumented.

## Status

There is a bit of work remaining (testing, validation, repackaging) but at least there are now binary file descriptions for `.wfm` files created by

* DS1000C untested
* DS1000E tested
* DS1000Z tested, wonky voltages
* DS4000 tested
* DS6000 untested

This has been a bit of an adventure.  In the process of nailing down the basic formats, I have gleaned information from a wide range of projects started by others.

* Shein's Pascal program <https://sourceforge.net/projects/wfmreader>
* Wagenaars's Matlab script <https://www.mathworks.com/matlabcentral/fileexchange/18999-read-binary-rigol-waveforms>
* Steele's C program <http://nsweb.tn.tudelft.nl/~gsteele/rigol2dat>
* Blaicher python code <https://github.com/mabl/pyRigolWFM>
* Szkutnik python code <https://github.com/michal-szkutnik/pyRigolWfm1000Z>
* Cat-Ion python code <https://github.com/Cat-Ion/rigol-ds4000-wfm>
* A LabView program I got from Rigol support
* Rigol's own documentation for 1000Z and 6000 file formats.


## Usage

Right now the first version of python module that supports 1000E and 1000Z formats (this is the pre-Kaitai Struct version!) can be installed via `pip`::

    pip install RigolWFM

Once this is done, one can extract signals from binary Rigol `.wfm` files by::

    import matplotlib.pyplot as plt
    import RigolWFM.wfm as rigol

    w = rigol.Wfm.from_file('OneChannelFile.wfm', 'DS1000E')
    ch = w.channel[0]
    plt.plot(ch.times, ch.volts)
    plt.show()

    w = rigol.Wfm.from_file('TwoChannelFile.wfm', 'DS1000Z')
    for ch in w.channels:
        plt.plot(ch.times, ch.volts, label=ch.name)
    plt.legend(loc='top right')
    plt.show()

