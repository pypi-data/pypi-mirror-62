# botw_havok

A library for converting Breath of the Wild Havok packfiles to JSON and back.

The main purpose of this library is deserializing Havok packfiles into a universal JSON file that can be converted to both Wii U and Switch packfiles.

Here's an example of HKX -> JSON conversion:
```py
from botw_havok import Havok

hk = Havok.from_file('A-1-0.hksc')
hk.to_json('A-1-0.json')
```

Here's an example of JSON -> HKX conversion:
```py
from botw_havok import Havok

hk = Havok.from_json('A-1-0.json')
hk.to_switch() # or hk.to_wiiu()
hk.to_file('A-1-0.hksc')
```

At the moment, only Havok Physics files (.hksc, .hkrb, .hktmrb) work. All of them should deserialize and serialize flawlessly and should be nearly identical to the originals (except the pointer section ordering which should be irrelevant).

The library is currently highly experimental, so expect bugs!

It's also really messy. Forgive me.
