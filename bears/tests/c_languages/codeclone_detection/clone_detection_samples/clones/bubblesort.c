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

// http://www.algorithmist.com/index.php/Bubble_sort.c
 void bubbleSort(int numbers[], int array_size)
{
  int i, j, temp;
  for (i = (array_size - 1); i > 0; i--)
  {
    for (j = 1; j <= i; j++)
    {
      if (numbers[j-1] > numbers[j])
      {
        temp = numbers[j-1];
        numbers[j-1] = numbers[j];
        numbers[j] = temp;
      }
    }
  }
}
