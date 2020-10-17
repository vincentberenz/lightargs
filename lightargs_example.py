
from lightargs import lightcoloring as lc

lc.format("\nWelcome to light coloring example",lc.green,lc.bright)

lc.format("This is a {} to have you {}\n",
          ("pleasure",lc.cyan),
          ("here",lc.blue),
          default=lc.dim)
