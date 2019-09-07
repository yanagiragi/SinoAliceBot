using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Threading;

namespace YrSinoAliceBot
{
    public class SinoAliceBot
    {
        private static int coordX;
        private static int coordY;

        private static string windowName = "SideSync";

        private IntPtr windowHandle = IntPtr.Zero;       

        private int osoujiX = 288;
        private int osoujiY = 168;

        public int homeX = 28;
        public int homeY = 623;

        private int osoujiConfirmX = 233;
        private int osoujiConfirmY = 605;

        public int delay = 1000;
        public int longDelay = 1000 * 3;

        public int rematchX = 107;
        public int rematchY = 600;

        // clockwise
        public int[] osoujiEnemyX =
        {
            167, // charcter 
            188,
            247,
            252,
            237,
            157,
            85,
            66,
            108
        };

        public int[] osoujiEnemyY =
        {
            362, // charcter 
            290,
            340,
            420,
            497,
            488,
            466,
            374,
            304
        };

        private Thread botThread;

        public SinoAliceBot()
        {
            bool result = GetWindow();

            Console.WriteLine(String.Format("Window Find: {0}\n", windowHandle));

            System.Diagnostics.Debug.Assert(result);

            // botThread = new Thread(new ThreadStart(this.Run));
            
        }

        public void ShowCursorPosition()
        {
            while (true)
            {
                Console.WriteLine(String.Format("Mouse Position = ({0}, {1})", MouseSimulator.Position.X, MouseSimulator.Position.Y));
                Thread.Sleep(1000);
            }
        }

        public void SingleLoop(int x, int y)
        {
            while (true)
            {
                MouseSimulator.Position = new Point(x, y);
                MouseSimulator.Click(MouseButton.Right);
                Thread.Sleep(10000);
            }
        }

        public void Run()
        {
            //Osouji();
            //LoopSingleStage();
            //ShowCursorPosition();
            SingleLoop(2793, 792);
        }

        public void LoopSingleStage()
        {
            int count = 0;

            while (count < 300)
            {
                // Press Home
                MouseSimulator.X = coordX + rematchX;
                MouseSimulator.Y = coordY + rematchY;
                Thread.Sleep(delay);

                MouseSimulator.Click(MouseButton.Left);
                Thread.Sleep(delay);

                ++count;
            }
        }

        public void EnterOsouji()
        {
            // Press Home
            MouseSimulator.X = coordX + homeX;
            MouseSimulator.Y = coordY + homeY;
            Thread.Sleep(delay);

            MouseSimulator.Click(MouseButton.Left);
            Thread.Sleep(longDelay);

            // Press Osouji Button
            MouseSimulator.X = coordX + osoujiX;
            MouseSimulator.Y = coordY + osoujiY;
            Thread.Sleep(delay);

            MouseSimulator.Click(MouseButton.Left);
            Thread.Sleep(delay);

            // Press Osouji Confirm Button
            MouseSimulator.X = coordX + osoujiConfirmX;
            MouseSimulator.Y = coordY + osoujiConfirmY;
            Thread.Sleep(delay);

            MouseSimulator.Click(MouseButton.Left);
            Thread.Sleep(longDelay * 2);
        }

        public void Osouji()
        {
            // Start
            int nowIndex = 0;
            
            int x = osoujiEnemyX[nowIndex];
            int y = osoujiEnemyY[nowIndex];

            MouseSimulator.X = coordX + x;
            MouseSimulator.Y = coordY + y;
            Thread.Sleep(delay);

            int count = 0;

            while (++count < 20)
            {
                x = osoujiEnemyX[nowIndex];
                y = osoujiEnemyY[nowIndex];

                MouseSimulator.X = coordX + x;
                MouseSimulator.Y = coordY + y;

                MouseSimulator.MouseDown(MouseButton.Left);
                Thread.Sleep(150);

                while (nowIndex < osoujiEnemyX.Length)
                {
                    x = osoujiEnemyX[nowIndex];
                    y = osoujiEnemyY[nowIndex];

                    MouseSimulator.X = coordX + x;
                    MouseSimulator.Y = coordY + y;

                    if (nowIndex == 0)
                    {
                        Thread.Sleep(150);
                        MouseSimulator.MouseUp(MouseButton.Left);
                        Thread.Sleep(150);
                        MouseSimulator.MouseDown(MouseButton.Left);
                        Thread.Sleep(150);
                    }
                    
                    Console.WriteLine(nowIndex);
                    
                    Thread.Sleep(150);

                    ++nowIndex;
                }

                Console.WriteLine("Done");

                MouseSimulator.MouseUp(MouseButton.Left);
                Thread.Sleep(2000);

                nowIndex = 0;
            }            
        }

        int Lerp(int start, int end, float delta)
        {
            float startF = (float)start;
            float endF = (float)end;
            return (int)Math.Ceiling(startF + (endF - startF) * delta);
        }

        public bool GetWindow()
        {
            this.windowHandle = WindowHandleHelper.GetHandleByProcessName(windowName);
            if (this.windowHandle == IntPtr.Zero)
            {
                Console.WriteLine("Windows Not Find");
                return false;
            }

            Rectangle lpRect = new Rectangle();
            WindowHandleHelper.GetClientRect(windowHandle, ref lpRect);
            Point lp = new Point();
            lp.X = lpRect.Left;
            lp.Y = lpRect.Top;

            WindowHandleHelper.ClientToScreen(windowHandle, ref lp);
            coordX = lp.X;
            coordY = lp.Y;

            WindowHandleHelper.SetForegroundWindow(windowHandle);

            if (coordX < 0 || coordY < 0)
            {
                Console.WriteLine("Windows Not Find");
                return false;
            }

            return true;
        }
    }
}
