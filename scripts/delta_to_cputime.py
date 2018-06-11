import sys
# hours/delta = 8*L^(3.78)
# hours = formula * delta
def calc_cpuhours(delta, size):
    # wrong since delta does not scale linearly with data
    return 8*pow(size, 3.78)*delta

print(calc_cpuhours(float(sys.argv[1]), float(sys.argv[2])))
