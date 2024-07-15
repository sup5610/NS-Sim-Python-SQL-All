using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace ModelThatJSONCorrectVersion
{
    class PopulationModel
    {
        public _PreyList[]? preyList { get; set; }
        public _PredList[]? predList { get; set; }
    }
    public class _PreyList
    {
        public _Rabbits[]? rabbits { get; set; }
        public _Deer[]? deer { get; set; }
    }
    public class _Rabbits
    {
        public int attack { get; set; }
        public int health { get; set; }
        public int speed { get; set; }
        public string guid { get; set; } = string.Empty;
    }
    public class _Deer
    {
        public int attack { get; set; }
        public int health { get; set; }
        public int speed { get; set; }
        public string guid { get; set; } = string.Empty;
    }
    public class _PredList
    {
        public _Wolves[]? wolves { get; set; }
        public _Jaguars[]? jaguars { get; set; }
    }
    public class _Wolves
    {
        public int attack { get; set; }
        public int health { get; set; }
        public int speed { get; set; }
        public string guid { get; set; } = string.Empty;
    }
    public class _Jaguars
    {
        public int attack { get; set; }
        public int health { get; set; }
        public int speed { get; set; }
        public string guid { get; set; } = string.Empty;
    }
}