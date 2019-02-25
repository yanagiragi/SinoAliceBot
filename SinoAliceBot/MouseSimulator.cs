using System.Drawing;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace YrSinoAliceBot
{
  public static class MouseSimulator
  {
    private const int MOUSEEVENTF_MOVE = 1;
    private const int MOUSEEVENTF_LEFTDOWN = 2;
    private const int MOUSEEVENTF_LEFTUP = 4;
    private const int MOUSEEVENTF_RIGHTDOWN = 8;
    private const int MOUSEEVENTF_RIGHTUP = 16;
    private const int MOUSEEVENTF_MIDDLEDOWN = 32;
    private const int MOUSEEVENTF_MIDDLEUP = 64;
    private const int MOUSEEVENTF_WHEEL = 2048;
    private const int MOUSEEVENTF_ABSOLUTE = 32768;

    [DllImport("user32.dll")]
    private static extern int ShowCursor(bool show);

    [DllImport("user32.dll")]
    private static extern void mouse_event(int flags, int dX, int dY, int buttons, int extraInfo);

    public static Point Position
    {
      get
      {
        return new Point(Cursor.Position.X, Cursor.Position.Y);
      }
      set
      {
        Cursor.Position = value;
      }
    }

    public static int X
    {
      get
      {
        return Cursor.Position.X;
      }
      set
      {
        Cursor.Position = new Point(value, MouseSimulator.Y);
      }
    }

    public static int Y
    {
      get
      {
        return Cursor.Position.Y;
      }
      set
      {
        Cursor.Position = new Point(MouseSimulator.X, value);
      }
    }

    public static void MouseDown(MouseButton button)
    {
      MouseSimulator.mouse_event((int) button, 0, 0, 0, 0);
    }

    public static void MouseDown(MouseButtons button)
    {
      switch (button)
      {
        case MouseButtons.Left:
          MouseSimulator.MouseDown(MouseButton.Left);
          break;
        case MouseButtons.Right:
          MouseSimulator.MouseDown(MouseButton.Right);
          break;
        case MouseButtons.Middle:
          MouseSimulator.MouseDown(MouseButton.Middle);
          break;
      }
    }

    public static void MouseUp(MouseButton button)
    {
      MouseSimulator.mouse_event((int) button * 2, 0, 0, 0, 0);
    }

    public static void MouseUp(MouseButtons button)
    {
      switch (button)
      {
        case MouseButtons.Left:
          MouseSimulator.MouseUp(MouseButton.Left);
          break;
        case MouseButtons.Right:
          MouseSimulator.MouseUp(MouseButton.Right);
          break;
        case MouseButtons.Middle:
          MouseSimulator.MouseUp(MouseButton.Middle);
          break;
      }
    }

    public static void Click(MouseButton button)
    {
      MouseSimulator.MouseDown(button);
      MouseSimulator.MouseUp(button);
    }

    public static void Click(MouseButtons button)
    {
      switch (button)
      {
        case MouseButtons.Left:
          MouseSimulator.Click(MouseButton.Left);
          break;
        case MouseButtons.Right:
          MouseSimulator.Click(MouseButton.Right);
          break;
        case MouseButtons.Middle:
          MouseSimulator.Click(MouseButton.Middle);
          break;
      }
    }

    public static void DoubleClick(MouseButton button)
    {
      MouseSimulator.Click(button);
      MouseSimulator.Click(button);
    }

    public static void DoubleClick(MouseButtons button)
    {
      switch (button)
      {
        case MouseButtons.Left:
          MouseSimulator.DoubleClick(MouseButton.Left);
          break;
        case MouseButtons.Right:
          MouseSimulator.DoubleClick(MouseButton.Right);
          break;
        case MouseButtons.Middle:
          MouseSimulator.DoubleClick(MouseButton.Middle);
          break;
      }
    }

    public static void MouseWheel(int delta)
    {
      MouseSimulator.mouse_event(2048, 0, 0, delta, 0);
    }

    public static void Show()
    {
      MouseSimulator.ShowCursor(true);
    }

    public static void Hide()
    {
      MouseSimulator.ShowCursor(false);
    }
  }
}
