using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace ModelThatJSONCorrectVersion
{
    public class Animal
    {
        public float Attack { get; set; }
        public float MaxHealth { get; set; }
        public float Speed { get; set; }
        public float ViewDistance { get; set; }
        public bool IsMale { get; set; }
        public string Guid { get; set; } = String.Empty;
        public bool isProgenitor { get; set; }
    }
}