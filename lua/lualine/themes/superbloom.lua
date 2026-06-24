local p = require("superbloom.palette")

return {
  normal = {
    a = { fg = p.base, bg = p.clarkia, gui = "bold" },
    b = { fg = p.text, bg = p.overlay },
    c = { fg = p.subtle, bg = p.surface },
  },
  insert = {
    a = { fg = p.base, bg = p.sage, gui = "bold" },
  },
  visual = {
    a = { fg = p.base, bg = p.lupine, gui = "bold" },
  },
  replace = {
    a = { fg = p.base, bg = p.paintbrush, gui = "bold" },
  },
  command = {
    a = { fg = p.base, bg = p.phacelia, gui = "bold" },
  },
  inactive = {
    a = { fg = p.muted, bg = p.surface },
    b = { fg = p.muted, bg = p.surface },
    c = { fg = p.muted, bg = p.surface },
  },
}
