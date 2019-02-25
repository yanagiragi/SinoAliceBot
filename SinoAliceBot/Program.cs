using System;

namespace SinoAlice
{
  internal static class Program
  {
    [STAThread]
    private static void Main()
    {
            YrSinoAliceBot.SinoAliceBot bot = new YrSinoAliceBot.SinoAliceBot();
            bot.Run();
    }
  }
}
