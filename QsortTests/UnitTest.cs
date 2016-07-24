using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using QuickSort;

namespace QsortTests
{
    [TestClass]
    public class UnitTest
    {
        [TestMethod]
        public void TestChooseMedian()
        {
            var input = new [] {8, 2, 4, 5, 7, 1};
            var expectedMedianIndex = 2;
            var actualMedianIndex = QsortHelpers.ChooseMedianAsPivotIndex(input, 0, input.Length - 1);
            Assert.IsTrue(expectedMedianIndex == actualMedianIndex);
        }
    }
}
