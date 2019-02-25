using System;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

namespace YrSinoAliceBot
{
  public static class WindowHandleHelper
  {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll ")]
    public static extern bool SetWindowText(IntPtr hwnd, string lpStrjng);

    [DllImport("user32.dll")]
    public static extern IntPtr GetActiveWindow();

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern int GetWindowRect(IntPtr hwnd, ref Rectangle lpRect);

    [DllImport("user32.dll")]
    public static extern IntPtr GetWindow(IntPtr hwnd, int cmd);

    [DllImport("user32.dll")]
    public static extern int GetTopWindow(IntPtr hwnd);

    [DllImport("user32.dll")]
    public static extern int SetParent(int hWndChild, int hWndNewParent);

    [DllImport("user32.dll")]
    public static extern int WindowFromPoint(int xPoint, int yPoint);

    [DllImport("user32.dll")]
    public static extern int GetClientRect(IntPtr hwnd, ref Rectangle lpRect);

    [DllImport("user32.dll")]
    public static extern bool ClientToScreen(IntPtr hWnd, ref Point lp);

    [DllImport("user32.dll")]
    public static extern bool ScreenToClient(IntPtr hWnd, ref Point lp);

    [DllImport("user32.dll")]
    public static extern IntPtr WindowFromPoint(Point p);

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int x, int y, int nWidth, int nHeight, bool BRePaint);

    [DllImport("user32.dll")]
    public static extern long GetWindowLong(IntPtr hWnd, int nlndex);

    [DllImport("user32.dll")]
    public static extern int GetClassName(IntPtr hWnd, StringBuilder classname, int nlndex);

    [DllImport("user32.dll")]
    public static extern int GetSystemMetrics(int nIndex);

    [DllImport("user32.dll")]
    public static extern bool SetWindowPos(IntPtr hWnd, int hWndInsertAfter, int X, int Y, int cx, int cy, int uFlags);

    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpszClass, string lpszWindow);

    [DllImport("user32.dll")]
    public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);

    [DllImport("gdi32.dll")]
    public static extern bool BitBlt(IntPtr hdcDest, int nXDest, int nYDest, int nWidth, int nHeight, IntPtr hdcSrc, int nXSrc, int nYSrc, int dwRop);

    public static IntPtr[] GetHandlesByProcessName(string strProcessName)
    {
      try
      {
        Process[] processesByName = Process.GetProcessesByName(strProcessName);
        IntPtr[] numArray = new IntPtr[processesByName.Length];
        for (int index = 0; index < processesByName.Length; ++index)
          numArray[index] = processesByName[index].MainWindowHandle;
        return numArray;
      }
      catch (Exception ex)
      {
        throw ex;
      }
    }

    public static IntPtr GetHandleByProcessName(string strProcessName)
    {
      try
      {
        Process[] processesByName = Process.GetProcessesByName(strProcessName);
        if (processesByName.Length == 1)
          return processesByName[0].MainWindowHandle;
        return IntPtr.Zero;
      }
      catch (Exception ex)
      {
        throw ex;
      }
    }

    public static void SetWindowPos(IntPtr hWnd)
    {
      WindowHandleHelper.SetWindowPos(hWnd, -1, 0, 0, 0, 0, 16387);
    }

    public static Bitmap windowFullScreen()
    {
      Graphics g = Graphics.FromHwnd(IntPtr.Zero);
      Bitmap bitmap = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height, g);
      Graphics graphics = Graphics.FromImage((Image) bitmap);
      IntPtr hdc1 = g.GetHdc();
      IntPtr hdc2 = graphics.GetHdc();
      WindowHandleHelper.BitBlt(hdc2, 0, 0, bitmap.Width, bitmap.Height, hdc1, 0, 0, 13369376);
      graphics.ReleaseHdc(hdc2);
      g.ReleaseHdc(hdc1);
      graphics.Dispose();
      g.Dispose();
      return bitmap;
    }
  }
}
