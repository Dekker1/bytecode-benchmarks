let rec fib n =
  if n <= 1 then n
  else fib (n-1) + fib (n-2);;

for it = 1 to 1000 do let _ = (fib 23) in () done
