# gpio-sysfs
Libraries to control GPIOs using the sysfs interface

## Compatibility

Now comptatible with all versions of Python !

## Install

pip install onion-gpio-sysfs

## Usage

        import onionGpio

# instantiate a GPIO object
gpio0 = onionGpio.OnionGpio(0)
# set to output direction with zero (LOW) being the default value
gpio0.setOutputDirection(0)
# get the vaule
gpio0.getValue()

For further examples look at python/examples/ folder.

## Author
Written by https://github.com/greenbreakfast

Python3 code adaptation by https://github.com/jdupl

PyPi package by https://github.com/grizmin
