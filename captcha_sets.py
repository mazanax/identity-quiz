import itertools

GROUP_CARS = 0
GROUP_CATS = 1
GROUP_DOGS = 2
GROUP_FISH = 3
GROUP_PLANES = 4
GROUP_TREES = 5

NAMES = ['cars', 'cats', 'dogs', 'fish', 'planes', 'trees']

GROUPS = [
    ["3b5b35n65.jpg", "46umn4bv.jpg", "635bvtv2t.jpg", "b245v245tb5.jpg", "b34t5356b.jpg", "mvc24vt.jpg",
     "oijouhgui42.jpg", "v2456b53nb3.jpg", "y35g452fr.jpg"],  # cars
    ["3n3n35n5.jpg", "b245325.jpg", "b24t635n.jpg", "b2t4tb5y.jpg", "b35635y.jpg", "nb35v34t5.jpg", "qrtb.jpg",
     "vafebq.jpg", "vwtr4.jpg"],  # cats
    ["3byrynu.jpg", "b3y5n3by.jpg", "bvb245.jpg", "h2h3h4j2.jpg", "i13i4i2.jpg", "mm24m52.jpg", "mzzz2x2x2.jpg",
     "n3565.jpg", "t235t23ti4.jpg"],  # dogs
    ["b2br5b5.jpg", "b36t342.jpg", "be48fe0d1.jpg", "e4152445ert.jpg", "t2b3b356.jpg", "u35465y3.jpg", "v442442.jpg",
     "w256h256.jpg", "y6357354.jpg"],  # fish
    ["2df525d.jpg", "8978gf6yuvibu.jpg", "by76tyghj.jpg", "d12rfr54.jpg", "h245g234f.jpg", "j25j2j34.jpg",
     "jii1ir43.jpg", "qefwrg.jpg", "t245g4g42.jpg"],  # planes
    ["2n2y5254t4.jpg", "b2g4tg2t4h.jpg", "bbb2542.jpg", "c341r34.jpg", "emmm523.jpg", "mm2m35m.jpg", "nbn145n34.jpg",
     "xx4133451.jpg", ""],  # tree
]

ALL = [
    "3g46h35yh.jpg", "3mb5m3.jpg", "465h7j.jpg", "b3456n.jpg", "b355n5.jpg", "b4t5h6gef.jpg", "bq45t5y25.jpg",
    "btrb453.jpg", "ebybytyet.jpg", "h2g543fr4.jpg", "htgwrvfetg56.jpg", "n35n35.jpg", "n634n65.jpg", "njib.jpg",
    "ravetfgbry.jpg", "twrbv.jpg", "u6735t4qfr3.jpg", "v37uy56g4wter.jpg", "v42t265.jpg",
    *itertools.chain.from_iterable(GROUPS)
]
