import cmath
from Crypto.Util.number import isPrime, long_to_bytes

q = int('9513 749018 075983 034085 918764 185242 949986 187938 391728 694055 305209 717744 257503 225678 393636 438369 553095 045978 207938 932347 555839 964566 376496 993702 806422 385729'.replace(' ', ''))
p = int('19253 294223 314315 727716 037086 964210 594461 001022 934798 241434 958729 430216 563195 726834 194376 256655 558434 205505 701941 181260 137383 350002 506166 062809 813588 037666'.replace(' ', ''))
p = p//2

hint = 461200758828450131454210143800752390120604788702850446626677508860195202567872951525840356360652411410325507978408159551511745286515952077623277648013847300682326320491554673107482337297490624180111664616997179295920679292302740410414234460216609334491960689077587284658443529175658488037725444342064697588997
ct = 8300471686897645926578017317669008715657023063758326776858584536715934138214945634323122846623068419230274473129224549308720801900902282047728570866212721492776095667521172972075671434379851908665193507551179353494082306227364627107561955072596424518466905164461036060360232934285662592773679335020824318918
assert isPrime(q)
e = 65537
d = pow(e, -1, (p-1)*(q-1))
print(long_to_bytes(pow(ct, d, p*q)))