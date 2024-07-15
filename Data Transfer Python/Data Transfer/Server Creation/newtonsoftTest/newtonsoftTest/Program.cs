using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Threading;


namespace newtonsoftTest
{
    public class Program
    {
        Thread mThread;
        public string connectionIP = "127.0.0.1";
        public int connectionPort = 64738;
        IPAddress localAdd;
        TcpListener listener;
        TcpClient client;

        bool running;

        private void Start()
        {
            ThreadStart ts = new ThreadStart(GetInfo);
            mThread = new Thread(ts);
            mThread.Start();
        }

        void GetInfo()
        {
            localAdd = IPAddress.Parse(connectionIP);
            listener = new TcpListener(IPAddress.Any, connectionPort);
            listener.Start();

            client = listener.AcceptTcpClient();

            running = true;
            while (running)
            {
                SendAndReceiveData();
            }
            listener.Stop();
        }

        void SendAndReceiveData()
        {
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];

            //---receiving Data from the Host----
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
            string recievedJson = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

            if (recievedJson != null)
            {
                //---Using received data---
                Console.WriteLine(recievedJson);

                //---Sending Data to Host----
                byte[] myWriteBuffer = Encoding.ASCII.GetBytes("Hey I got your message Python! Do You see this message?"); //Converting string to byte data
                nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length); //Sending the data in Bytes to Python
            }
        }
    }
}