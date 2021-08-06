import pytest

import board_mock
import lcd_mock

board_class = board_mock

def test_lcd_create():
  # the mock LCD doesn't use it's inputs, real or None inputs should work
  lcd_1 = lcd_mock.LCD(None, None, None, None, None, None, None)
  lcd_2 = lcd_mock.LCD(rs=board_class.D27,
        backlight=board_class.D15,
        enable=board_class.D22,
        d4=board_class.D18,
        d5=board_class.D23,
        d6=board_class.D24,
        d7=board_class.D25,)

  assert lcd_1 != None
  assert lcd_2 != None

def test_lcd_begin(capsys):
  lcd_1 = lcd_mock.LCD(None, None, None, None, None, None, None)
  lcd_2 = lcd_mock.LCD(None, None, None, None, None, None, None)
  
  lcd_1.begin(20, 4)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "*====================*\n")

  lcd_2.begin(10, 2)
  captured = capsys.readouterr()
  assert captured.out == ("*==========*\n"
                       +  "|          |\n"
                       +  "|          |\n"
                       +  "*==========*\n")

  assert lcd_1.cols == 20
  assert lcd_2.cols == 10
  assert lcd_1.rows == 4
  assert lcd_2.rows == 2

def test_lcd_no_begin():
  lcd = lcd_mock.LCD(None, None, None, None, None, None, None) 

  # print without using begin() first
  with pytest.raises(lcd_mock.UninitializedLCDError):
    lcd.print("This should fail", 1, 1)

def test_lcd_print(capsys):
  lcd = lcd_mock.LCD(None, None, None, None, None, None, None) 
  lcd.begin(20,4)

  # Flush the current stdout buffer from begin() output
  _ = capsys.readouterr()

  # print into the first line
  lcd.print("test string 1", 1, 1)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|test string 1       |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "*====================*\n")

  # print into the first line again
  lcd.print("test string 1", 1, 1)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|test string 1       |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "*====================*\n")
  
  # print into the second line
  lcd.print("test string 2", 2, 2)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|test string 1       |\n"
                       +  "|   test string 2    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "*====================*\n")
  
  # print into the third line
  lcd.print("test string 3", 3, 3)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|test string 1       |\n"
                       +  "|   test string 2    |\n"
                       +  "|       test string 3|\n"
                       +  "|                    |\n"
                       +  "*====================*\n")
  
  # print into the fourth line, too long
  lcd.print("test string 4 oh no this one's too long", 4, 1)
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|test string 1       |\n"
                       +  "|   test string 2    |\n"
                       +  "|       test string 3|\n"
                       +  "|test string 4 oh no this one's too long|\n"
                       +  "*====================*\n")

def test_lcd_clear(capsys):
  lcd = lcd_mock.LCD(None, None, None, None, None, None, None) 
  
  # test that a 20x4 empty box is properly shown on 
  lcd.begin(20,4)
  lcd.print("test string", 1, 2)
  lcd.print("test string", 2, 2)
  lcd.print("test string", 3, 2)
  lcd.print("test string", 4, 2)

  # Flush the current stdout buffer from begin() and prints
  _ = capsys.readouterr()

    # clear the LCD again
  lcd.clear()
  captured = capsys.readouterr()
  assert captured.out == ("*====================*\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "|                    |\n"
                       +  "*====================*\n")