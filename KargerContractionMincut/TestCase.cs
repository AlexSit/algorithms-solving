using System.Collections.Generic;

namespace KargerContractionMincut
{
    public class TestCase
    {
        public string FilePath { get; set; }
        public Dictionary<int, List<int>> Input { get; set; }
        public long Answer { get; set; }
    }
}
