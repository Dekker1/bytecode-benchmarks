function int: tak(int: x, int: y, int: z) =
  if y < x then
    tak(tak(x-1,y,z), tak(y-1,z,x), tak(z-1,x,y))
  else z endif;

constraint forall (i in 1..1000) (let {int: comp = tak(18, 12, 6); } in true );
