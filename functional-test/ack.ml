let rec ack x y = match (x,y) with
    | (0, _) -> y + 1
    | (_ , 0) -> ack (x - 1) 1
    | (_, _) -> ack (x - 1) (ack x (y - 1));;

for it = 1 to 1000 do let _ = (ack 3 6) in () done