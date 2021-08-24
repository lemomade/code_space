rate=24
in_frame=79

r = in_frame % rate
seconds = in_frame / rate

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
r = r/rate*1000.0
out_seconds = "%02d:%02d:%02d,%03d" % (h, m, s, r)
print(out_seconds)