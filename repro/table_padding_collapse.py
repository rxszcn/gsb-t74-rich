import io, re
from rich.console import Console
from rich.table import Table
from rich.cells import cell_len


def first_line(t, W=60):
    c = Console(file=io.StringIO(), width=W, color_system=None)
    c.print(t)
    return c.file.getvalue().rstrip("\n").split("\n")[0]


def probe(label, padding, collapse, pad_edge, w=6, n=3):
    t = Table(box=None, padding=padding, collapse_padding=collapse,
              show_header=False, expand=False, pad_edge=pad_edge)
    for _ in range(n):
        t.add_column(width=w)
    t.add_row(*["ABCDEFGHIJ"] * n)
    line = first_line(t)
    runs = re.findall(r"[A-Z…]+", line)
    widths = [cell_len(r) for r in runs]
    lead = len(line) - len(line.lstrip())
    # inter-run whitespace runs
    gaps = [len(g) for g in re.findall(r"(?<=\S) +(?=\S)", line)]
    trailing = len(line) - len(line.rstrip())
    print("  %-34s lead=%d widths=%s gaps=%s tail=%d | %r"
          % (label, lead, widths, gaps, trailing, line))


print("### pad=(0,1), declared width=6 x3")
for collapse in (False, True):
    for pad_edge in (True, False):
        probe("collapse=%s pad_edge=%s" % (collapse, pad_edge),
              (0, 1), collapse, pad_edge)

print("### pad=(0,1,0,4) left-heavy, width=6 x3")
for collapse in (False, True):
    for pad_edge in (True, False):
        probe("collapse=%s pad_edge=%s" % (collapse, pad_edge),
              (0, 1, 0, 4), collapse, pad_edge)

print("### pad=(0,3,0,1) right-heavy, width=6 x3")
for collapse in (False, True):
    for pad_edge in (True, False):
        probe("collapse=%s pad_edge=%s" % (collapse, pad_edge),
              (0, 3, 0, 1), collapse, pad_edge)

print("### real-world shape: two columns width=8, header, collapse=True pad_edge=True")
t = Table(box=None, collapse_padding=True, padding=(0, 1), show_header=True, pad_edge=True)
t.add_column("name", width=8)
t.add_column("value", width=8)
t.add_row("abcdefghij", "1234567890")
c = Console(file=io.StringIO(), width=40, color_system=None)
c.print(t)
for l in c.file.getvalue().rstrip("\n").split("\n"):
    print("   %r" % l)
