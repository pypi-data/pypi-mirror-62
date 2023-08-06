========
xtk_demo
========

Demo plugin to show very basic integration of girder and XTK

Installation
------------

1) install plugin::

    pip install girder-xtk-demo
    girder build
    girder serve

3) upload data. For example ``MRHead.nrrd``

4) Add ``XTK`` metadata to newly created item.

Possible value for `XTK` metadata are::

    {"type": "volume"}
    {"type": "volume2d"}
    {"type": "mesh"}


Note: ``mesh`` type will not work for ``MRHead.nrrd``

5) Refresh the page. Et voila.


Examples
--------

Type: volume
++++++++++++

`girder-xtk-type-volume <https://cloud.githubusercontent.com/assets/219043/8861580/30b94064-3159-11e5-861e-922c0c8c3684.png>`_

Type: volume2d
++++++++++++++

`girder-xtk-type-volume2d <https://cloud.githubusercontent.com/assets/219043/8861583/3466922a-3159-11e5-9471-f7294a29a40f.png>`_



