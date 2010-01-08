function [y] = invchr(string,position)
y = string;
if string(position) == '0'
    y(position) = '1';
else
    y(position) = '0';
end
  