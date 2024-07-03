# TTS模块
- 利用语音合成技术，生成所有古诗的mp3音频。此处使用的是讯飞语音合成功能。

## text_speech_synthesis.py
- 该文件主要利用讯飞的长文本的语音合成功能
  - output_all_poems.py 首先将poems全部导出到poems_file中
  - poems_file_format.py 对poems_file的文件进行格式化 导出到poems_file_fmt
  - 执行 text_speech_synthesis.py 生成mp3文件到mp3目录下