
# Mood-Ring
Mood-ring object to return a user's mood with available configurations - practice for packaging and distributing software.

# Installation

Mood-ring can be installed with pip:

`pip install mood-ring`

# Documentation

The ring class can be instantiated and used as a string to display a mood.

```
>>> from mood_ring import Ring
>>>
>>> r = Ring()
>>> print(r)
active
```
The Ring class comes with the following options:
- stressed
- nervous
- unsettled
- active
- relaxed
- lovable
- romantic
- happy
- tired
- calm
### Methods
The **change** method will update the mood of the ring object.

NOTE: When using the change method, the mood will be reset to a different option than currently selected - there is no chance the same mood option will be set again.

```
>>> r = Ring()
>>> str(r)
'tired'
>>> r.change()
>>> str(r)
'unsettled'
```
If the possibility of the same outcome is desired, instantiate a new instance of the Ring object.
```
>>> r = Ring(); str(r)
'stressed'
>>> r = Ring(); str(r)
'stressed'
```
### Custom User-Inputs
To over-write the default outputs, am optional list argument can be accepted to specify the pool of output options the class will output.

```
>>> r = Ring(['suave', 'sophisticated'])
>>> str(r)
'suave'
```
To retain the default output list while also adding user-defined outputs, the optional keyword argument 'extend' can accept a list of strings to extend the out-of-the-box behavior.
```
>>> r = Ring(extend=['million bucks'])
>>> str(r)
'tired'
```
### Weighted User-Inputs
Either of the above arguments can also be passed a dictionary that weights the probability of a certain option being picked - keys are mood option names, and values are weights. In the example below, 'mad' has a 1/5 chance of being returned and 'happy' has a 4/5 chance of being returned.
```
>>> r = Ring({'mad': 1, 'happy': 4})
>>> str(r)
'happy'
```
NOTE: The 10 default options are weighted with 1. If using the 'extend' keyword, setting a key as weight 1 gives it equal probability as the original options.
```
>>> # New option weighted equally with default options
>>> r = Ring(extend={'dopey': 1})
>>> str(r)
'stressed'
>>>
>>> # New option weighted 99x as likely of returning as defaults
>>> r = Ring(extend={'dopey': 99})
>>> str(r)
'dopey'
```
