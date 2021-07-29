let rec tak x y z =
  if y < x then
    tak (tak (x-1) y z) (tak (y-1) z x) (tak (z-1) x y)
  else z;;

for it = 1 to 1000 do let _ = (tak 18 12 6) in () done
