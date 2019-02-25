// Decompiled with JetBrains decompiler
// Type: MMDModelPreviewGenerator_MMM.GlobalHotKeyHelper
// Assembly: MMDModelPreviewGenerator_MMM, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 2E6FECA2-2147-4ADE-8A9E-FAD9F45D0D25
// Assembly location: D:\_Downloads\MMDModelPreviewGenerator_MMM\MMDModelPreviewGenerator_MMM\MMDModelPreviewGenerator_MMM.exe

using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace MMDModelPreviewGenerator_MMM
{
  public static class GlobalHotKeyHelper
  {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, GlobalHotKeyHelper.KeyModifiers fsModifiers, Keys vk);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    [Flags]
    public enum KeyModifiers
    {
      None = 0,
      Alt = 1,
      Ctrl = 2,
      Shift = 4,
      WindowsKey = 8,
    }
  }
}
