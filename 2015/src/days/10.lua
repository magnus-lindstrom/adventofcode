local u = require 'src/utils'

local function tbl_from_str_2(str)
  local tbl = {}
  for i = 1, #str do
    table.insert(tbl, tonumber(str:sub(i,i)))
  end
  return tbl
end

local function evolve_tbl_2(tbl)
  local output = {}
  local current_digit = tbl[1]
  local reps = 1

  for i = 2, u.table_length(tbl) do
    if current_digit == tbl[i] then
      reps = reps + 1
    else -- a digit streak is broken
      output[#output+1] = reps
      output[#output+1] = current_digit
      current_digit = tbl[i]
      reps = 1
    end

  end
  -- add last streak since it won't be added in the loop
  output[#output+1] = reps
  output[#output+1] = current_digit

  return output
end

local function main(times)
  -- Keep a table representation of the string where the values define the string
  -- So, 1121 would be the table
  -- {
  --     {1: 1},
  --     {2: 1},
  --     {3: 2},
  --     {4: 1},
  -- }
  --
  -- Use 2 tables to not have to create new tables and have them grow dynamically, which takes time
  local str = u.lines_from('inputs/10')[1]
  local tbl1 = tbl_from_str_2(str)
  local tbl2 = {}
  local tbl_nr_in_use = 1

  for _ = 1, times do
    if tbl_nr_in_use == 1 then
      tbl2 = evolve_tbl_2(tbl1)
      tbl_nr_in_use = 2
    else
      tbl1 = evolve_tbl_2(tbl2)
      tbl_nr_in_use = 1
    end
  end
  return math.max(#tbl1, #tbl2)
end

local function a()
  return main(40)
end

local function b()
  return main(50)
end

return {a = a, b = b}
