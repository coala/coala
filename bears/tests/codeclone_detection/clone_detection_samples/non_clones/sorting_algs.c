// Numerous sorting algorithms from wikibooks.org. Code clone detection shall
// not detect different sort algorithms as clones.

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

// https://en.wikibooks.org/wiki/Algorithm_Implementation/Sorting/Gnome_sort#C
void gnome_sort(int *array, int size){
    int i, tmp;
    for(i=1; i<size; ){
        if(array[i-1] <= array[i])
            ++i;
        else{
            tmp = array[i];
            array[i] = array[i-1];
            array[i-1] = tmp;
            --i;
            if(i == 0)
                i = 1;
        }
    }
}

// http://de.wikibooks.org/wiki/Algorithmen_und_Datenstrukturen_in_C/_Mergesort
// a good example for bad code
 void MergeSort(int liste[], int groesse){

     if(groesse > 1){

         int haelfte1[groesse/2];
         int haelfte2[(groesse + 1)/2];
         int i;
         for(i = 0; i < groesse/2; ++i)
             haelfte1[i] = liste[i];
         for(i = groesse/2; i < groesse; ++i)
             haelfte2[i - groesse/2] = liste[i];

         MergeSort(haelfte1,groesse/2);
         MergeSort(haelfte2,(groesse + 1)/2);

         int *pos1 = &haelfte1[0];
         int *pos2 = &haelfte2[0];
         for(i = 0; i < groesse; ++i){
             if(*pos1 <= *pos2){
                 liste[i] = *pos1;
                 if (pos1 != &haelfte2[(groesse+1)/2 - 1]) { // pos1 nicht verändern, wenn der größte Wert mehrmals vorkommt
                     if(pos1 == &haelfte1[groesse/2 - 1]){
                         pos1 = &haelfte2[(groesse+1)/2 - 1];
                     }
                     else{
                         ++pos1;
                     }
                 }
             }
             else{
                 liste[i] = *pos2;
                 if(pos2 == &haelfte2[(groesse + 1)/2 - 1]){
                     pos2 = &haelfte1[groesse/2 - 1];
                 }
                 else{
                     ++pos2;
                 }
             }
         }
     }
 }

// http://de.wikibooks.org/wiki/Algorithmen_und_Datenstrukturen_in_C/_Selectionsort
void selectionsort(int *const data, size_t const n) {
	size_t left = 0;
	while (left < n) {
		size_t min = left;
		size_t i;
		for (i = left+1; i < n; ++i) {
			if (data[i] < data[min]) {
				min = i;
			}
		}
		int tmp = data[min];
		data[min] = data[left];
		data[left++] = tmp;
	}
}

// http://de.wikibooks.org/wiki/Algorithmen_und_Datenstrukturen_in_C/_Bubblesort
 void bubblesort(int *array, int length)
 {
     int i, j;
     for (i = 0; i < length - 1; ++i)
     {

 	for (j = 0; j < length - i - 1; ++j)
        {
 	    if (array[j] > array[j + 1])
            {
 		int tmp = array[j];
 		array[j] = array[j + 1];
 		array[j + 1] = tmp;
 	    }
 	}
     }
 }

// https://en.wikibooks.org/wiki/Algorithm_Implementation/Sorting/Insertion_sort
void insertSort(int a[], int length)
{
    int i, j, value;

    for(i = 1; i < length; i++)
    {
        value = a[i];
        for (j = i - 1; j >= 0 && a[j] > value; j--)
        {
            a[j + 1] = a[j];
        }
        a[j + 1] = value;
    }
}

// https://de.wikibooks.org/wiki/Algorithmen_und_Datenstrukturen_in_C/_Quicksort
void quicksort(int *begin, int *end)
{
    int *ptr;
    int *split;
    if (end - begin <= 1)
        return;
    ptr = begin;
    split = begin + 1;
    while (++ptr <= end) {
        if (*ptr < *begin) {
            swap(ptr, split);
            ++split;
        }
    }
    swap(begin, split - 1);
    quicksort(begin, split - 1);
    quicksort(split, end);
}
