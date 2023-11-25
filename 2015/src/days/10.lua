local u = require 'src/utils'

local function tbl_from_str(str)
  local tbl = {}
  local i = 1
  local index = 1
  while i <= str:len() do
    local digit = str:sub(i,i)
    local reps = 1
    for j = i + 1, str:len() do
      if str:sub(j,j) == digit then
        reps = reps + 1
      else
        break
      end
    end
    tbl[index] = {[reps] = tonumber(digit)}
    index = index + 1
    i = i + reps
  end
  return tbl
end

local function tbl_from_str_2(str)
  local tbl = {}
  for i = 1, #str do
    table.insert(tbl, tonumber(str:sub(i,i)))
  end
  return tbl
end

local function evolve_tbl(table)
  local output = {}
  local current_digit
  local reps
  local i = 0 -- start at 0 because first index must be 1 for ipairs to work later

  for _, inner_table in ipairs(table) do
    for k, v in pairs(inner_table) do
      if k == current_digit then
        reps = reps + 1
      else
        if current_digit ~= nil then
          output[i] = {[reps] = current_digit}
        end
        i = i + 1
        current_digit = k
        reps = 1
      end

      if v == current_digit then
        reps = reps + 1
      else
        output[i] = {[reps] = current_digit}
        i = i + 1
        current_digit = v
        reps = 1
      end
    end
  end
  output[i] = {[reps] = current_digit}
  return output
end

local function evolve_tbl_2(tbl)
  local output = {}
  local current_digit = tbl[1]
  local reps = 1
  -- print('before for loop. cur_dig:', current_digit, 'reps:', reps)

  for i = 2, u.table_length(tbl) do
    -- print(string.format('i: %d, current_digit: %d, tbl[i]: %d', i, current_digit, tbl[i]))
    if current_digit == tbl[i] then
      reps = reps + 1
    else -- a digit streak is broken
      output[#output+1] = reps
      output[#output+1] = current_digit
      current_digit = tbl[i]
      reps = 1
    end
    -- print('after for loop. reps:', reps)

  end
  -- add last streak since it won't be added in the loop
  output[#output+1] = reps
  output[#output+1] = current_digit

  return output
end

local function str_len_from_tbl(table)
  local len = 0
  for _, inner_table in ipairs(table) do
    for k, v in pairs(inner_table) do
      local nr_as_string = tostring(v)
      len = len + k * nr_as_string:len()
    end
  end
  return len
end

local function str_len_from_tbl_2(tbl)
  local len = 0
  for i = 1, u.table_length(tbl), 2 do
    len = len + tbl[i]
  end
  return len
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

-- print(a())
-- print(b())

return {a = a, b = b}
