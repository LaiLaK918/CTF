n = 137695652953436635868173236797773337408441001182675256086214756367750388214098882698624844625677992374523583895607386174643756159168603070583418054134776836804709359451133350283742854338177917816199855370966725059377660312824879861277400624102267119229693994595857701696025366109135127015217981691938713787569
peek = 6745414226866166172286907691060333580739794735754141517928503510445368134531623057
c = 60939585660386801273264345336943282595466297131309357817378708003135300231065734017829038358019271553508356563122851120615655640023951268162873980957560729424913748657116293860815453225453706274388027182906741605930908510329721874004000783548599414462355143868922204060850666210978837231187722295496753756990

R.<x> = PolynomialRing(Zmod(n))
f = x + (peek<<240)
p = int(f.small_roots(X=2**240, beta=0.5, epsilon=1/35)[0] + (peek<<240))
q = n//p
d = pow(65537,-1,(p-1)*(q-1))
from Crypto.Util.number import long_to_bytes
long_to_bytes(int(pow(c, d, n)))