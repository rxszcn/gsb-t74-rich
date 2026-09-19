import io
from rich.console import Console
from rich.table import Table
from rich.cells import cell_len

def render(t, W=60):
    c = Console(file=io.StringIO(), width=W, color_system=None)
    c.print(t)
    return c.file.getvalue().rstrip("\n").split("\n")

def build(collapse, padding=(0, 1), n=3, w=6):
    t = Table(box=None, padding=padding, collapse_padding=collapse, show_header=False,
              expand=False, pad_edge=True)
    for _ in range(n):
        t.add_column(width=w)
    t.add_row(*["ABCDEFGHIJ"] * n)
    return t

print("padding=(0,1)  [the DEFAULT table padding], 3 columns each declared width=6")
print(" collapse=False:", ["%r" % l for l in render(build(False))])
print(" collapse=True :", ["%r" % l for l in render(build(True))])
print()
print(" _get_padding_width collapse=True :", [build(True)._get_padding_width(i) for i in range(3)])
print(" _get_padding_width collapse=False:", [build(False)._get_padding_width(i) for i in range(3)])
print()
print("### per-column content cell count (what the user asked for: 6)")
for collapse in (False, True):
    line = render(build(collapse))[0]
    # split on the padding pattern is messy; instead measure each run of letters
    import re
    runs = re.findall(r"[A-Z…]+", line)
    print("  collapse=%s content runs -> %s  (widths %s)" % (collapse, runs, [cell_len(r) for r in runs]))
print()
print("### left-heavy padding (0,1,0,4)")
for collapse in (False, True):
    print("  collapse=%s -> %r" % (collapse, render(build(collapse, padding=(0, 1, 0, 4)))[0]))
print()
print("### real-world shape: two columns of text, collapse_padding=True")
t = Table(collapse_padding=True, padding=(0, 1), show_header=True, box=None)
t.add_column("name", width=8)
t.add_column("value", width=8)
t.add_row("abcdefghij", "1234567890")
for l in render(t):
    print("   %r" % l)
