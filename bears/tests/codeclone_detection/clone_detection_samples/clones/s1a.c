void original(int n) {
float sum=0.0; //C1
float prod=1.0;
for (int i=1; i<=n; i++)
    {sum=sum + i;
    prod = prod * i;
    foo(sum, prod); }}

void sumProd(int n) {
float sum=0.0; //C1
float prod=1.0;
for (int i=1; i<=n; i++)
      {sum=sum + i;
      prod = prod * i;
      foo(sum, prod); }}
