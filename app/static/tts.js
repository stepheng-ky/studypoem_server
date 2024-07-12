$(document).ready(function() {
  $('#generate-btn').click(function() {
    $('#filename-display').text('生成语音中...');
    $('#overlay').show();
    $('#loading').show();
    var text = $('#text-input').val();
    $.ajax({
      type: "POST",
      url: "/studypoem/tts",
      data: JSON.stringify({ text: text, voice: "x3_xiaodu", speed: 40, mp3_filename: "tts" }),
      contentType: "application/json",
      success: function(response) {
        $('#overlay').hide();
        $('#loading').hide();
        alert("语音生成成功：" + response);
        $('#play-btn').attr("disabled", false);
        $('#download-btn').attr("disabled", false);
        $('#pause-btn').attr("disabled", true);
        $('#play-btn').attr("data-filename", response);
        $('#download-btn').attr("data-filename", response);
        $('#filename-display').text('当前语音文件是：' + response + '.mp3');
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $('#overlay').hide();
        $('#loading').hide();
        alert("请求失败：" + textStatus + "，错误：" + errorThrown);
      }
    });
  });

  $('#play-btn').click(function() {
    var filename = $(this).attr("data-filename");
    $.ajax({
      type: "GET",
      url: "/studypoem/play/tts/" + filename,
      success: function(response) {
        var audio = document.getElementById("audio-player");
        audio.src = "/studypoem/play/tts/" + filename;
        audio.play();
        $('#generate-btn').attr("disabled", true);
        $('#play-btn').attr("disabled", true);
        $('#pause-btn').attr("disabled", false);
        audio.addEventListener('ended', function() {
          $('#generate-btn').attr("disabled", false);
          $('#play-btn').attr("disabled", false);
          $('#pause-btn').attr("disabled", true);
        });
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log("播放失败：" + textStatus + "，错误：" + errorThrown);
      }
    });
  });

  $('#pause-btn').click(function() {
      var audio = document.getElementById("audio-player");
      if (audio.paused) {
          audio.play();
          $('#play-btn').attr("disabled", true);
          $('#pause-btn').attr("disabled", false);
          $('#generate-btn').attr("disabled", true);
      } else {
          audio.pause();
          $('#play-btn').attr("disabled", false);
          $('#pause-btn').attr("disabled", true);
          $('#generate-btn').attr("disabled", false);
      }
  });

  $('#download-btn').click(function() {
    var filename = $(this).attr("data-filename");
    window.location.href = "/studypoem/download/" + filename + ".mp3";
  });
});