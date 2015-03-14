load Sort.hack,
output-file Sort.out,
compare-to Sort.cmp,
output-list RAM[2]%D2.6.2 RAM[3]%D2.6.2 RAM[4]%D2.6.2 RAM[5]%D2.6.2 RAM[6]%D2.6.2 RAM[7]%D2.6.2 RAM[8]%D2.6.2 RAM[9]%D2.6.2;

set PC 0,
set RAM[2] 14,
set RAM[3] 16,
set RAM[4] 8,
set RAM[5] 20,
set RAM[14] 2,
set RAM[15] 4;
repeat 1000 {
  ticktock;
}
output;


set PC 0,
set RAM[2] 10,
set RAM[3] 11,
set RAM[4] 17,
set RAM[5] 13,
set RAM[14] 2,
set RAM[15] 4;
repeat 1000 {
  ticktock;
}
output;


set PC 0,
set RAM[2] 10,
set RAM[3] 11,
set RAM[4] 19,
set RAM[5] 13,
set RAM[6] 22,
set RAM[7] 18,
set RAM[8] 14,
set RAM[9] 12,
set RAM[14] 2,
set RAM[15] 8;
repeat 1500 {
  ticktock;
}
output;


set PC 0,
set RAM[2] 16,
set RAM[3] 11,
set RAM[4] 29,
set RAM[5] 13,
set RAM[6] 20,
set RAM[7] 18,
set RAM[8] 19,
set RAM[9] 33,
set RAM[14] 2,
set RAM[15] 8;
repeat 2000 {
  ticktock;
}
output;


set PC 0,
set RAM[2] 10,
set RAM[3] 14,
set RAM[4] 19,
set RAM[5] 11,
set RAM[6] 20,
set RAM[7] 18,
set RAM[8] 12,
set RAM[9] 31,
set RAM[14] 2,
set RAM[15] 8;
repeat 2000 {
  ticktock;
}
output;



