import subtractionMethod
taggs = [
    'u4_skip_0',
    'u4_skip_4',
    'u4_skip_4_8',
    'u4_skip_128',
    'u4_skip_4_128',
    ]

rem_idx = [[], [0], [0,1], [5],[0, 5]]

avals = [
        [1.24451187,1.24451188],
        [1.24446457,1.24446458],
        [1.24536273,1.24536274],
        [1.24235242,1.24235243],
        [1.24235242,1.24235243],
        ]

for t,ix,a in zip(taggs,rem_idx,avals):
    subtractionMethod.subtract_A_between(a[0],a[1],t,ix)
