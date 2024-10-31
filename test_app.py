#-*- coding:utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from app import ClickAutomationApp

class TestClickAutomationApp(unittest.TestCase):
    @patch('app.filedialog.askdirectory', return_value='test_directory')
    @patch('app.messagebox.showinfo')
    def test_select_images_directory(self, mock_showinfo, mock_askdirectory):
        app = ClickAutomationApp(MagicMock())
        app.select_images_directory()
        self.assertEqual(app.images_directory, 'test_directory')
        mock_showinfo.assert_called_once_with("信息", "选择的图片目录: test_directory")

    @patch('app.requests.get')
    @patch('app.messagebox.showinfo')
    def test_fetch_instructions_success(self, mock_showinfo, mock_requests_get):
        mock_response = MagicMock()
        mock_response.text = "Instructions content"
        mock_requests_get.return_value = mock_response

        app = ClickAutomationApp(MagicMock())
        app.fetch_instructions()
        mock_showinfo.assert_called_once_with("说明", "Instructions content")

    @patch('app.requests.get')
    @patch('app.messagebox.showerror')
    def test_fetch_instructions_failure(self, mock_showerror, mock_requests_get):
        mock_requests_get.side_effect = Exception("Network Error")
        app = ClickAutomationApp(MagicMock())
        app.fetch_instructions()
        mock_showerror.assert_called_once_with("错误", "无法获取说明: Network Error")

    @patch('app.filepath.askopenfilename', return_value='test_image.png')
    @patch('app.messagebox.showinfo')
    def test_select_can_throw_image(self, mock_showinfo, mock_askopenfilename):
        app = ClickAutomationApp(MagicMock())
        app.select_can_throw_image()
        self.assertEqual(app.can_throw_image, 'test_image.png')
        mock_showinfo.assert_called_once_with("信息", "选择的投降条件图片: test_image.png")

    @patch('app.find_and_click', return_value=True)
    @patch('app.pyautogui.press')
    def test_start_clicking_surrender(self, mock_press, mock_find_and_click):
        app = ClickAutomationApp(MagicMock())
        app.images_directory = 'test_directory'
        app.can_throw_image = 'test_image.png'
        app.close_threshold.set(1)  # Set threshold for testing
        app.is_running = True
        app.start_clicking_thread()  # Start the clicking thread
        app.start_clicking()  # Directly call the clicking method for testing
        self.assertEqual(app.surrender_count.get(), 1)
        mock_press.assert_called_once_with('esc')

    def test_toggle_clicking_starts(self):
        app = ClickAutomationApp(MagicMock())
        app.images_directory = 'test_directory'
        app.can_throw_image = 'test_image.png'
        app.toggle_clicking()
        self.assertTrue(app.is_running)

    def test_toggle_clicking_stops(self):
        app = ClickAutomationApp(MagicMock())
        app.is_running = True
        app.toggle_clicking()
        self.assertFalse(app.is_running)

if __name__ == '__main__':
    unittest.main()

