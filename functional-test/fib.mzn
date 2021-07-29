
function int: fib(int: n) =
  if n <= 1 then n
  else fib(n-1) + fib(n-2) endif;

constraint forall(i in 1..1000) (let {int: comp = fib(23);} in true);
