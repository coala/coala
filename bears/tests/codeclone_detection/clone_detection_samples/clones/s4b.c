// Adapted from Roy, C.K., Cordy, J.R., and Koschke, R. Comparison and
// evaluation of code clone detection techniques and tools: A qualitative
// approach. Science of Computer Programming 74, 7 (2009), 470–495.

void foo(float, float);

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
    {prod = prod * i;
    sum=sum + i;
    foo(sum, prod); }}
