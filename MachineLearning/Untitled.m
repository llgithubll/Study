%% define
A = [-4, 1.9, -3.2, -12; -0.25, 2, 9, 0.3; 0.1, 7, -1, 5]
B = [-1, 0; 2, 3; -2, 1; 0, -1]

%% calu
C = A*B

%% logical
a = 4
a > 3 & a < 10

%% conditional data selection
I = A<0
r = A(I)

%% if_else
x = -5:5

%% for
yy(1) = 1;
for n = 1:6
    yy(n+1) = yy(n) - 0.1*yy(n)
end
x = 1:7
yy
plot(x, yy)

%% while
amount(1) = 1000;
r = 0.08;
p = 1;
while amount(p) < 2000
    amount(p+1) = amount(p)*(r+1);
    p = p+1;
end
p