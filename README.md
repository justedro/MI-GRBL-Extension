# MI GRBL Inkscape Extension

This project is aimed to resurrect the unsupported <a href="https://gitlab.com/inkscape/inkscape">Inkscape</a>
extension that is used to generate G-codes out of vector images to feed the
<a href="https://www.thingiverse.com/thing:2349232">GRBL-powered pen plotters</a>.
Fixed and checked on Python 3.9 and Inkscape 1.1.1.

The source version was found somewhere in the internet. The first commit represents it as is.
It did not support Python 3 which is a requirement for Inkscape 1.0+.

## Supported GRBL versions
The firmware that supports the generated code is <a href="https://github.com/robottini/grbl-servo">here</a>.

It uses the commands M03 Sxxx (xxx between 0 and 255) to rotate the servo between 0-180 (down the pen). The command M05 is to turn the servo to zero degrees (lift the pen).

# Contribution
Is welcome. The missing things at the moment:
* cleaner code + removal of deprecated methods
* tests
* packaging
* example drawings

# License
GNU General Public License v2+
Previous authors listed in the beginning of the source files.