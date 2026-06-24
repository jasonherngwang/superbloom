local M = {}

local function clear_package_cache()
  for name in pairs(package.loaded) do
    if name == "superbloom" or name:match("^superbloom%.") then
      package.loaded[name] = nil
    end
  end
end

function M.colorscheme()
  vim.cmd("hi clear")

  if vim.fn.exists("syntax_on") == 1 then
    vim.cmd("syntax reset")
  end

  vim.o.termguicolors = true
  vim.o.background = "dark"
  vim.g.colors_name = "superbloom"

  require("superbloom.theme").apply()
end

function M.reload()
  clear_package_cache()
  vim.cmd.colorscheme("superbloom")
end

vim.api.nvim_create_user_command("SuperbloomReload", function()
  require("superbloom").reload()
end, { force = true })

return M
