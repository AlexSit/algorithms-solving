using System;
using System.Collections.Generic;

namespace QuickSort
{
    public static class QsortHelpers
    {
        public static int ChooseMedianAsPivotIndex(int[] input, int leftIndex, int rightIndex)
        {
            if (rightIndex == leftIndex)
                throw new Exception("Can't choose pivot! Array length is 0!");

            var firstIndex = ChooseFirstAsPivotIndex(leftIndex, rightIndex);
            var first = input[firstIndex];

            var lastIndex = ChooseLastAsPivotIndex(leftIndex, rightIndex);
            var last = input[lastIndex];

            int middleIndex;
            if ((rightIndex - leftIndex + 1)%2 != 0)
            {
                middleIndex = ((rightIndex - leftIndex) / 2) + leftIndex;
            }
            else
            {
                middleIndex = ((rightIndex - leftIndex + 1) / 2) - 1 + leftIndex;
            }
            var middle = input[middleIndex];

            var pivotCandidates = new List<Tuple<int, int>>()
            {
                new Tuple<int, int>(first, firstIndex),
                new Tuple<int, int>(last, lastIndex),
                new Tuple<int, int>(middle, middleIndex)
            };

            var comparer = new PivotCandidatesComparer();
            pivotCandidates.Sort(comparer);

            return pivotCandidates[1].Item2;
        }

        public static int ChooseFirstAsPivotIndex(int leftIndex, int rightIndex)
        {
            if (rightIndex == leftIndex)
                throw new Exception("Can't choose pivot! Array length is 0!");

            return leftIndex;
        }

        public static int ChooseLastAsPivotIndex(int leftIndex, int rightIndex)
        {
            if (rightIndex == leftIndex)
                throw new Exception("Can't choose pivot! Array length is 0!");

            return rightIndex;
        }
    }

    public class PivotCandidatesComparer : IComparer<Tuple<int, int>>
    {
        public int Compare(Tuple<int, int> x, Tuple<int, int> y)
        {
            if (x.Item1 == y.Item1)
                return 0;

            if (x.Item1 < y.Item1)
                return -1;

            if (x.Item1 > y.Item1)
                return 1;

            throw new Exception();
        }
    }
}
