using System;
using System.Globalization;

namespace ModelThatJSON
{
    internal class MyModel
    {
        public int cid { get; set; }
        public string entityName { get; set; }
        public _Accounts accounts { get; set; }
    }
    public class _Accounts
    {
        public _USA usa { get; set; }
        public _Slovakia slovakia { get; set; }
        public _Ecuador ecuador { get; set; }
        public _Mexico mexico { get; set; }
    }
    public class _USA
    {
        public _EntityStockShares entityStockShares { get; set; }
    }
    public class _Slovakia
    {
        public _EntityStockShares entityStockShares { get; set; }
    }
    public class _Ecuador
    {
        public _EntityStockShares entityStockShares { get; set; }
    }
    public class _Mexico
    {
        public _EntityStockShares entityStockShares { get; set; }
    }

    public class _EntityStockShares
    {
        public string label { get; set; }
        public string desc { get; set; }
        public _Units units { get; set; }
    }
    public class _Units
    {
        public _Trades[] trades { get; set; }
    }


    public class _Trades
    {
        public int acct { get; set; }
        public DateTime dateOfTrade { get; set; }
        public string ticker { get; set; }
        public string tranType { get; set; }
        public int qty { get; set; }
        public decimal costPerShare { get; set; }
    }

}