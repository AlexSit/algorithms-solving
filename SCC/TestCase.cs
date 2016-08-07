using System;
using System.Collections.Generic;

namespace SCC
{
    public class TestCase
    {
        public string FilePath { get; set; }
        public List<Tuple<int,int>> Input { get; set; }
        public int[] Answer { get; set; }
    }
}
