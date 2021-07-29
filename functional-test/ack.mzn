function int: ack(int: m, int: n) =
  if m == 0 then
    n + 1
  elseif n == 0 then
    ack(m-1, 1)
  else
    ack(m-1, ack(m, n-1))
  endif;

constraint forall (i in 1..1000) (let {int: comp = ack(3,6);} in true);

% constraint trace("\(ack(4,2))\n");
